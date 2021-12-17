import re
import os
import functools

from xml.etree.ElementTree import XML, Element
from typing import (
    Union,
    Pattern,
    Callable,
    Any,
    Type,
    Tuple,
    Iterator,
    Dict,
    IO,
    List,
)

__all__: List[str] = [
    "read_gcp_prefix_format_list",
    "GTINError",
    "CheckDigitError",
    "calculate_check_digit",
    "append_check_digit",
    "has_valid_check_digit",
    "validate_check_digit",
    "get_gcp",
    "GTIN",
]

_NON_NUMERIC_CHARACTERS_PATTERN: Pattern = re.compile(r"[^\d]")
_GCP_PREFIX_FORMAT_LIST_PATH: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "GCPPrefixFormatList.xml"
)

lru_cache: Callable[..., Any] = functools.lru_cache


def _remove_non_numeric_characters(gtin: str) -> str:
    """
    Strip non-numeric characters from a string
    """
    return _NON_NUMERIC_CHARACTERS_PATTERN.sub("", gtin)


def _prefix_length_element_filter(element: Element) -> bool:
    return ("prefix" in element.attrib) and ("gcpLength" in element.attrib)


def read_gcp_prefix_format_list() -> Element:
    file_io: IO[str]
    with open(_GCP_PREFIX_FORMAT_LIST_PATH, "rt", encoding="utf-8") as file_io:
        return XML(file_io.read())


@lru_cache()
def _get_prefixes_gcp_lengths() -> Dict[str, int]:
    """
    This function obtains a dictionary mapping GTIN prefixes to integers
    indicating the character length for GCPs which begin with each prefix.
    """
    prefixes_gcp_lengths: Dict[str, int] = {}
    root: Element = read_gcp_prefix_format_list()
    element: Element
    for element in filter(_prefix_length_element_filter, root):
        prefixes_gcp_lengths[element.attrib["prefix"]] = int(
            element.attrib["gcpLength"]
        )
    return prefixes_gcp_lengths


class GTINError(Exception):
    def __init__(self, gtin: str, message: str) -> None:
        self.gtin: str = gtin
        super().__init__(message)


class CheckDigitError(GTINError, ValueError):
    def __init__(self, invalid_gtin: str, correct_check_digit: str) -> None:
        super().__init__(
            gtin=invalid_gtin,
            message=(
                f'"{invalid_gtin}" is not a valid GTIN, the last digit is '
                f'"{invalid_gtin[-1]}", whereas the correct check-digit '
                f'would be "{correct_check_digit}".'
            ),
        )


def calculate_check_digit(unchecked_gtin: Union[str, int]) -> Union[str, int]:
    """
    The function calculates a check-digit from a raw GTIN. The type of
    return value reflects the type of the `unchecked_gtin` argument provided
    (either an `int` or `str`).

    Implementation Details:

    A check-digit is calculated from the preceding digits by
    multiplying the sum of every 2nd digit *from right to left* by 3,
    adding that to the sum of all the other digits (1st, 3rd, etc.),
    modulating the result by 10 (find the remainder after dividing by 10),
    and subtracting *that* result *from* 10.
    """
    assert isinstance(unchecked_gtin, (str, int))
    type_: Union[Type[str], Type[int]] = type(unchecked_gtin)
    # Remove non-numeric characters
    if isinstance(unchecked_gtin, str):
        unchecked_gtin = _remove_non_numeric_characters(unchecked_gtin)
    # Reverse the digits
    digits: Tuple[str, ...] = tuple(d for d in reversed(str(unchecked_gtin)))
    # Do the math
    return type_(
        str(
            10
            - (  # From 10 we substract...
                (
                    # The sum of every 2nd digit, multiplied by 3
                    (sum(int(d) for d in digits[::2]) * 3)
                    +
                    # The sum of every 2nd digit, offset by 1
                    (sum(int(d) for d in digits[1::2]))
                )
                % 10  # Modulo 10 (the remainder after dividing by 10)
            )
        )[-1]
    )


def append_check_digit(unchecked_gtin: Union[str, int]) -> Union[str, int]:
    """
    This function accepts a GTIN sans-check-digit and returns the same
    GTIN *with* its check-digit.
    """
    type_: Union[Type[str], Type[int]] = type(unchecked_gtin)
    assert issubclass(type_, (str, int))
    return type_(
        f"{str(unchecked_gtin)}{str(calculate_check_digit(unchecked_gtin))}"
    )


def has_valid_check_digit(gtin: Union[int, str]) -> bool:
    """
    Provided a GTIN (of any length, as either a `str` or `int`), determine
    if the check digit is valid.
    """
    gtin = str(gtin)
    return gtin[-1] == calculate_check_digit(gtin[:-1])


def validate_check_digit(gtin: Union[int, str]) -> None:
    """
    If the provided `gtin` does not have a valid check-digit, this
    function raises an error.
    """
    gtin = str(gtin)
    check_digit: str = calculate_check_digit(gtin[:-1])  # type: ignore
    if gtin[-1] != check_digit:
        raise CheckDigitError(gtin, check_digit)


def _lookup_gcp_length(prefix: str) -> int:
    """
    Recursively lookup shorter prefixes until a GCP length for that
    prefix is identified
    """
    if prefix == "":
        return 0
    return _get_prefixes_gcp_lengths().get(
        prefix, _lookup_gcp_length(prefix[:-1])
    )


def get_gcp(gtin: Union[int, str]) -> str:
    """
    This function returns the company prefix for the provided GTIN.

    GCP Information: https://www.gs1.org/standards/id-keys/company-prefix
    """
    # Get the 14-digit variation of this GTIN, since the GCP is based on the
    # GTIN-14
    gtin = str(gtin)
    length: int = len(gtin)
    if length < 14:
        leading_zeros: str = "0" * (14 - length)
        gtin = f"{leading_zeros}{gtin}"
    # Lookup the GCP length for this GTIN's prefix, then add `1` to come up
    # with the value for the `stop` argument for the prefix slice
    stop: int = _lookup_gcp_length(gtin[1:-1]) + 1
    # The value for `start` is `1` because the GCP starts *after* the indicator
    # digit of a GTIN-14
    return gtin[1:stop]


def _validate_gtin_arguments(
    gtin: Union[str, int] = "", length: int = 0, raw: Union[str, int] = ""
) -> None:
    if not isinstance(gtin, (str, int)):
        raise TypeError(
            "The `gtin` parameter must receive an `int` or `str`, not "
            f"{repr(gtin)}"
        )
    if not isinstance(length, int):
        raise TypeError(
            f"The `length` parameter must receive an `int`, not {repr(gtin)}"
        )
    if not isinstance(raw, (str, int)):
        raise TypeError(
            "The `raw` parameter must receive an `int` or `str`, not "
            f"{repr(raw)}"
        )
    if not (gtin == "" or raw == ""):
        raise ValueError(
            "Either a `gtin` or a `raw` argument may be provided, but not both"
        )


def _harmonize_gtin_arguments(
    gtin: Union[str, int] = "", length: int = 0, raw: Union[str, int] = ""
) -> Tuple[str, int, str]:
    if isinstance(gtin, str):
        if gtin != "":
            gtin = _remove_non_numeric_characters(gtin)
            if not length:
                length = len(gtin)
    else:
        gtin = str(gtin)
    if isinstance(raw, str):
        if raw != "":
            raw = _remove_non_numeric_characters(raw)
            if not length:
                length = len(raw) + 1
    else:
        raw = str(raw)
    # If a length isn't provided and can't be inferred, assume it's a GTIN-14
    if not length:
        length = 14
    # Get the raw GTIN from the complete GTIN, if the latter was provided
    if gtin and not raw:
        raw = gtin[:-1]
    # Add leading zeros, if needed
    text_length: int = len(raw) + 1
    if text_length < length:
        leading_zeros: str = "0" * (length - text_length)
        raw = f"{leading_zeros}{raw}"
    return gtin, length, raw


@lru_cache(typed=True)
def _parse_gtin(
    gtin: Union[str, int] = "", raw: Union[str, int] = "", length: int = 0
) -> Tuple[str, str, str, str, int]:
    """
    This function is used to parse arguments for a `GTIN`, when the object is
    being created by a user (as opposed to being un-pickled).
    """
    _validate_gtin_arguments(gtin=gtin, length=length, raw=raw)
    gtin, length, raw = _harmonize_gtin_arguments(
        gtin=gtin, length=length, raw=raw
    )
    # Calculate the check-digit, either to complete or validate the GTIN
    check_digit: str = calculate_check_digit(raw)  # type: ignore
    # If a `gtin` was provided, the calculated `check_digit` should match
    if gtin and check_digit != gtin[-1]:
        raise CheckDigitError(gtin, check_digit)
    gtin = f"{raw}{check_digit}"
    gcp: str = get_gcp(gtin)
    indicator_digit: str = gtin[-14] if length > 13 else "0"
    item_reference_start: int = len(gcp) - 13
    item_reference: str = gtin[item_reference_start:-1]
    return indicator_digit, gcp, item_reference, check_digit, length


class GTIN:
    """
    This class represents a Global Trade Item Number, an identifier which can
    be used to:

    - Identify a trade item's GCP (GS1 Company Prefix), Item Reference, and
      Indicator Digit
    - Validate a GTIN's check-digit
    - Calculate a check-digit from a raw GTIN
    """

    __slots__: Tuple[str, ...] = (
        "indicator_digit",
        "gcp",
        "item_reference",
        "check_digit",
        "length",
    )

    def __init__(
        self,
        gtin: Union[str, int] = "",
        length: int = 0,
        raw: Union[str, int] = "",
        # These private parameters should only be used when
        # pickling/un-pickling a GTIN
        _indicator_digit: str = "",
        _gcp: str = "",
        _item_reference: str = "",
        _check_digit: str = "",
    ) -> None:
        """
        Parameters:

        - gtin (str|int|float): A GTIN *with* a check-digit
        - length (int): The number of digits represented by the GTIN
          (this overrides the inferred length if greater than zero)
        - raw (str|int): A GTIN *without* a check-digit
        """
        if not (
            _indicator_digit
            and _gcp
            and _item_reference
            and _check_digit
            and length
        ):
            (
                _indicator_digit,
                _gcp,
                _item_reference,
                _check_digit,
                length,
            ) = _parse_gtin(gtin=gtin, length=length, raw=raw)
        self.indicator_digit: str = _indicator_digit
        self.gcp: str = _gcp
        self.item_reference: str = _item_reference
        self.check_digit: str = _check_digit
        self.length: int = length

    def __reduce__(
        self,
    ) -> Tuple[Type["GTIN"], Tuple[str, int, str, str, str, str, str]]:
        return self.__class__, (
            "",
            self.length,
            "",
            self.indicator_digit,
            self.gcp,
            self.item_reference,
            self.check_digit,
        )

    def __len__(self) -> int:
        return self.length

    def __int__(self) -> int:
        return int(str(self))

    def __float__(self) -> float:
        return float(str(self))

    def __iter__(self) -> Iterator[str]:
        return iter(
            (
                self.indicator_digit,
                self.gcp,
                self.item_reference,
                self.check_digit,
            )
        )

    def __str__(self) -> str:
        start: int = -self.length
        return "".join(self)[start:]

    def __hash__(self) -> int:
        return int(str(self)) + 100000000000000 * self.length

    def __repr__(self) -> str:
        return (
            f"{self.__module__}."
            f"{self.__class__.__name__}"
            f'("{str(self)}")'
        )
