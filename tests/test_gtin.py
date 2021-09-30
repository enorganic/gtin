import unittest
from subprocess import getstatusoutput
from typing import Union, Dict, Optional
from itertools import starmap
from gtin import (
    _get_prefixes_gcp_lengths,  # noqa
    GTIN,
    get_gcp,
    calculate_check_digit,
    CheckDigitError,
    has_valid_check_digit,
    validate_check_digit,
)


def run(command: str, echo: bool = True) -> str:
    """
    This function runs a shell command, raises an error if a non-zero
    exit code is returned, and echo's both the command and output *if*
    the `echo` parameter is `True`.

    Parameters:

    - command (str): A shell command
    - echo (bool) = True: If `True`, the command and the output from the
      command will be printed to stdout
    """
    if echo:
        print(command)
    status: int
    output: str
    status, output = getstatusoutput(command)
    # Create an error if a non-zero exit status is encountered
    if status:
        raise OSError(output)
    else:
        output = output.strip()
        if output and echo:
            print(output)
    return output


def _test_calculate_check_digit(
    raw: Union[int, str], check_digit: Union[int, str]
) -> None:
    _test_library_calculate_check_digit(raw, check_digit)
    _test_cli_calculate_check_digit(raw, check_digit)


def _test_cli_calculate_check_digit(
    raw: Union[int, str], check_digit: Union[int, str]
) -> None:
    check_digit = str(check_digit)
    calculated_check_digit: str = run(f"gtin ccd {str(raw)}")
    assert calculated_check_digit == check_digit, (
        f"The check-digit for {raw} should be {check_digit}, "
        f"not {calculated_check_digit}"
    )


def _test_library_calculate_check_digit(
    raw: Union[int, str], check_digit: Union[int, str]
) -> None:
    check_digit = int(check_digit)
    calculated_check_digit: int = int(calculate_check_digit(raw))
    assert calculated_check_digit == check_digit, (
        f"The check-digit for {raw} should be {check_digit}, "
        f"not {calculated_check_digit}"
    )


def _test_gtin_check_digit(
    raw: Union[int, str], check_digit: Union[int, str]
) -> None:
    check_digit = int(check_digit)
    calculated_check_digit: int = int(GTIN(raw=raw).check_digit)
    assert calculated_check_digit == check_digit, (
        f"The check-digit for {raw} should be {check_digit}, "
        f"not {calculated_check_digit}"
    )


class TestGTIN(unittest.TestCase):
    """
    This test case validates functionality for the `gtin` library and CLI.
    """

    def test_calculate_check_digit(self) -> None:
        list(
            starmap(
                _test_calculate_check_digit,
                (
                    (890123456789, 0),
                    (10101, 1),
                    (567898901234, 2),
                    (82957399425, 3),
                    (5936663101, 4),
                    (15059928976, 5),
                    (901234567890, 6),
                    (36013101, 7),
                    (123456789012, 8),
                    (208957399425, 9),
                ),
            )
        )

    def test_gtin_check_digit(self) -> None:
        list(
            starmap(
                _test_gtin_check_digit,
                (
                    (890123456789, 0),
                    (10101, 1),
                    (567898901234, 2),
                    (82957399425, 3),
                    (5936663101, 4),
                    (15059928976, 5),
                    (901234567890, 6),
                    (36013101, 7),
                    (123456789012, 8),
                    (208957399425, 9),
                ),
            )
        )

    def test_gtin_str(self) -> None:
        # region 14-digit
        # str  - implicit length
        assert str(GTIN(raw="0123456789012")) == "01234567890128"
        # str - explicit length
        assert str(GTIN(raw="0123456789012", length=14)) == "01234567890128"
        # int - implicit length
        assert str(GTIN(raw=123456789012)) == "01234567890128"
        # int - explicit length
        assert str(GTIN(raw=123456789012, length=14)) == "01234567890128"
        # endregion
        # region 12-digit
        # str - implicit length
        assert str(GTIN(raw="01234567890")) == "012345678905"
        # str - explicit length
        assert str(GTIN(raw="01234567890", length=12)) == "012345678905"
        # int
        assert str(GTIN(raw=1234567890, length=12)) == "012345678905"
        # endregion
        # region 8-digit
        # str - implicit length
        assert str(GTIN(raw="0123456")) == "01234565"
        # str - explicit length
        assert str(GTIN(raw="0123456", length=8)) == "01234565"
        # int
        assert str(GTIN(raw=123456, length=8)) == "01234565"
        # endregion
        # region Parameter Validation
        # Verify that an invalid type throws an error
        error_type: type = object
        # float - implicit length
        # (intentionally passing an incorrect type of argument)
        try:
            GTIN(raw=123456789012.0)  # type: ignore
        except TypeError as error:
            error_type = type(error)
        assert issubclass(error_type, TypeError)
        # endregion

    def test_gtin_gcp(self) -> None:
        prefixes_gcp_lengths: Dict[str, int] = _get_prefixes_gcp_lengths()
        assert prefixes_gcp_lengths
        # GS1 Global Office
        assert prefixes_gcp_lengths["951"] == 0
        # Demo prefixes
        assert prefixes_gcp_lengths["9523"] == 6
        assert prefixes_gcp_lengths["9524"] == 7
        assert prefixes_gcp_lengths["9525"] == 8
        assert prefixes_gcp_lengths["9526"] == 9
        assert prefixes_gcp_lengths["9527"] == 10
        assert prefixes_gcp_lengths["9528"] == 11
        assert prefixes_gcp_lengths["9529"] == 12
        # GS1 US
        assert prefixes_gcp_lengths["060"] == 7
        # ISBN
        assert prefixes_gcp_lengths["978"] == 0
        assert prefixes_gcp_lengths["979"] == 0
        # Parse known GTINs
        assert (
            GTIN("00332100000001").gcp == get_gcp("00332100000001") == "033210"
        )
        assert run("gtin gcp 00332100000001") == "033210"
        # Restricted circulation within a *region*
        assert prefixes_gcp_lengths["200"] == 0
        assert prefixes_gcp_lengths["200"] == 0
        # Test restricted circulation GTINs
        assert GTIN("02345678901289").gcp == get_gcp("02345678901289") == ""
        assert run("gtin gcp 02345678901289") == ""
        assert GTIN("00234567890129").gcp == get_gcp("00234567890129") == ""
        assert run("gtin gcp 00234567890129") == ""
        # Test a missing GCP
        assert GTIN("01345678901280").gcp == get_gcp("01345678901280") == ""
        assert run("gtin gcp 01345678901280") == ""

    def test_has_valid_check_digit(self) -> None:
        assert has_valid_check_digit("02345678901289")
        assert run("gtin hvcd 02345678901289") == "YES"
        assert not has_valid_check_digit("02345678901281")
        assert run("gtin hvcd 02345678901281") == "NO"

    def test_validate_check_digit(self) -> None:
        # Ensure that valid check-digits don't raise an error
        validate_check_digit("02345678901289")
        run("gtin vcd 02345678901289")
        # Ensure that invalid check-digits *do* raise an error
        caught_error: Optional[Exception] = None
        try:
            validate_check_digit("02345678901281")
        except Exception as error:  # noqa
            caught_error = error
        assert isinstance(caught_error, CheckDigitError)
        caught_error = None
        try:
            run("gtin vcd 02345678901281")
        except Exception as error:  # noqa
            caught_error = error
        assert isinstance(caught_error, OSError)


if __name__ == "__main__":
    unittest.main()
