"""
A library for parsing GTINs ("Global Trade Item Numbers"--also known as UPC/EAN/JAN/ISBN).

Author: David Belais <david@belais.me>
License: MIT
"""

# Python 2 compatibility
from __future__ import division
from future.standard_library import install_aliases
install_aliases()
from future.utils import python_2_unicode_compatible
from builtins import int, bytes, str

import re
from numbers import Number
from gtin.gcp import GCP_PREFIXES


class GTINError(Exception):
    pass


class CheckDigitError(GTINError, ValueError):
    pass


@python_2_unicode_compatible
class GTIN:
    """
    gtin
    ====

    A python package for parsing GTINs ("Global Trade Item Numbers"--also known as UPC/EAN/JAN/ISBN).

    To install::

    $ pip install gtin

    gtin.GTIN
    ---------

    This class represents a Global Trade Item Number, and can be used to:

    - Identify a trade item's GCP (GS1 Company Prefix), Item Reference, and Indicator Digit.
    - Validate a GTIN's check-digit.
    - Calculate a check-digit from a raw GTIN.

    **Parameters**:

    :gtin:

        A string or number representing a GTIN, including the check-digit.

        - When the *gtin* parameter is provided, the last (rightmost) digit is used to validate the GTIN if
          no value is provided for the parameter *check_digit*.

    :length:

        The length of the GTIN.

        - If no value is passed for *length*, and *gtin* is a *str*--*length* is inferred based on the character
          length of *gtin*.
        - If no value is passed for *length*, *gtin* is *None*, and *raw* is a *str*--*length* is inferred based
          on the length of *raw* (adding 1, to account for the absent check-digit).
        - If no length is passed, and none can be inferred from *gtin* or *raw*, *length* defaults to 14.

    :raw:

        A string or number representing the GTIN, excluding the check-digit.

        - If a value is provided for the parameter *gtin*, this parameter is not used, but is instead derived
          from *gtin*.

    In lieu of passing a complete GTIN, with or without the check-digit, using the above parameters--it is possible to
    pass the components of the GTIN separately: the indicator digit, GCP (GS1 Company Prefix), item reference, and
    (optionally) the check-digit.

    :indicator_digit:

        This is the first (leftmost) digit of a GTIN-14.

        - "0" indicates a base unit.
        - "1" through "8" are used to define the packaging hierarchy of a product with the same item reference.
        - "9" indicates a variable-measure trade item.

    :gcp:

        The GS1 Company Prefix is a globally unique identifier assigned to a company by GS1 Member Organizations to
        create the identification numbers of the GS1 System. Company Prefixes, which vary in length, are comprised
        of a GS1 Prefix and a Company Number.

    :item_reference:

        The item reference is the part of the GTIN that is allocated by the user to identify a trade item for a
        given Company Prefix. The Item Reference varies in length as a function of the Company Prefix length.

    :check_digit:

        A mod-10 algorithm digit used to check for input errors. To understand how this digit is calculated, refer
        to: http://www.gs1.org/how-calculate-check-digit-manually. If this parameter is provided, it is matched
        against the calculated check-digit, and an error is raised if it does not match the calculated check-digit.

    Examples
    ```

    >>> from gtin import GTIN

    A *GTIN* initialized without any arguments:

    >>> print(repr(GTIN()))
    gtin.GTIN('00000000000000')

    Typical usage will require converting your *GTIN* to a *str* prior to use in your application.

    >>> print(str(GTIN()))
    00000000000000

    Given a raw GTIN, the check-digit is calculated and appended.

    >>> print(str(GTIN(raw='0978289450809')))
    09782894508091

    Given a valid GTIN *str* for *gtin*, the return value of *str(GTIN(gtin))* is equal to *gtin*.

    >>> print(str(GTIN('04000101613600')))
    04000101613600

    Non-numeric characters are ignored/discarded.

    >>> print(str(GTIN('0-4000101-61360-0')))
    04000101613600

    Given a an *int* for the parameter *raw*, the length defaults to 14.

    >>> print(str(GTIN(raw=7447010150)))
    00074470101505

    >>> print(str(GTIN(74470101505)))
    00074470101505

    Given a GTIN, and a length:

    >>> print(str(GTIN(raw=7447010150, length=12)))
    074470101505

    >>> print(str(GTIN(74470101505, length=12)))
    074470101505

    >>> print(str(GTIN('74470101505', length=14)))
    00074470101505

    Get the GCP of a GTIN:

    >>> print(GTIN('00041333704647').gcp)
    0041333

    >>> print(GTIN('00811068011972').gcp)
    081106801

    >>> print(GTIN('00188781000171').gcp)
    0188781000

    Get the component parts of a *GTIN* instance as a tuple containing
    *GTIN.indicator_digit*, *GTIN.gcp*, *GTIN.item_reference*, and *GTIN.check_digit*:

    >>> print(tuple(GTIN(raw='0400010161360')))
    ('0', '4000101', '61360', '0')

    ```
    """

    def __init__(
        self,
        gtin=None,  # type: Optional[Union[str, int]] = None
        length=None,  # type: Optional[Union[int]] = None
        raw=None  # type: Optional[Union[str, int]] = None
    ):
        self._gtin = None  # type: Optional[str]
        self._gcp = None
        self._check_digit = None
        self._raw = None
        self._length = length
        self._indicator_digit = None
        self._item_reference = None

        data = gtin or raw

        if data is not None:

            if isinstance(data, (str, bytes)):
                data = self._normalize(data)
                if gtin:
                    self._raw = int(data[:-1])
                    if self._length is None:
                        self._length = len(data)
                else:
                    self._raw = int(data)
                    if self._length is None:
                        self._length = len(data) + 1
            elif isinstance(data, int):
                data = str(abs(int(data)))
                if gtin:
                    gtin = data
                    self._raw = int(data[:-1])
                else:
                    self._raw = data
                if self._length is None:
                    self._length = 14
            else:
                raise TypeError(
                    'The `gtin` provided must be a `str` or `int`, not `%s`.' % repr(data)
                )

        if gtin and self.check_digit != gtin[-1]:
            raise CheckDigitError(
                ('This GTIN ("%s") has an invalid check-digit ("%s"). ' % (gtin, gtin[-1])) +
                ('The correct check-digit would be "%s".' % self.check_digit)
            )

    @staticmethod
    def _normalize(gtin):
        # type: (Union[str, bytes]) -> str
        """
        Strip non-numeric characters from a string
        """
        if isinstance(gtin, bytes):
            data = str(gtin, encoding='utf-8', errors='ignore')
        gtin = re.sub(r'[^\d]', '', gtin)
        if not gtin:
            raise GTINError(
                '%s is not a valid GTIN. ' % repr(gtin) +
                'A GTIN should contain 1 or more numeric digits.'
            )
        return gtin

    def __len__(self):
        # type: () -> int
        return self.length

    @property
    def length(self):
        # type: () -> int
        return self._length

    @length.setter
    def length(self, length):
        # type: (int) -> None
        self._gtin = None
        self._length = length

    @property
    def raw(self):
        # type: () -> int
        return self._raw

    @raw.setter
    def raw(self, value):
        # type: (Union[str, Number]) -> None
        self.__init__(raw=value, length=self.length)

    @property
    def check_digit(self):
        # type: () -> Optional[str]
        if self._check_digit is None:
            if self.raw is None:
                return None
            digits = tuple(d for d in reversed(str(self.raw)))
            return str(
                10 - (
                    (
                        (sum(int(d) for d in digits[::2]) * 3) +
                        (sum(int(d) for d in digits[1::2]))
                    ) % 10
                )
            )[-1]
        return self._check_digit

    @property
    def gcp(self):
        # type: () -> Optional[str]
        """
        Return the GCP corresponding to this GTIN, or an empty string if no GCP can be identified
        """

        if self._gcp is None:

            # Get the 14-digit variation of this GTIN
            gtin = str(self)  # type: str
            if len(gtin) < 14:
                gtin = ('0' * (14 - len(gtin))) + gtin

            # Lookup the GCP length for this GTIN's prefix
            prefix = gtin[1:-1]  # type: str
            prefix_length = None  #type: Optional[int]
            while prefix and (prefix_length is None):
                if prefix in GCP_PREFIXES:
                    prefix_length = GCP_PREFIXES[prefix]
                else:
                    prefix = prefix[:-1]

            return gtin[1:1 + prefix_length] if prefix else ''

        return self._gcp

    @property
    def indicator_digit(self):
        # type: () -> Optional[str]
        """
        The indicator digit is the first digit of a GTIN-14
        """
        return (
            str(self)[0]
            if self.length == 14 else
            ''
        )

    @property
    def item_reference(self):
        # type: () -> Optional[str]
        """
        The "item reference" comprises the portion of a GTIN following the GCP (GTIN company prefix), and preceding the
        check digit.
        """
        return str(self)[len(self.gcp) + 1:-1]

    def __int__(self):
        # type: () -> int
        return int(str(self))

    def __float__(self):
        # type: () -> float
        return float(str(self))

    def __str__(self):
        # type: () -> str
        if self._gtin is None:
            if self.raw is None:
                return '0' * self.length
            gtin = str(self.raw) + self.check_digit
            self._gtin = (
                ('0' * (self.length - len(gtin))) +
                gtin
            )
        return self._gtin

    def __hash__(self):
        # type: () -> int
        return self.raw or 0

    def __repr__(self):
        # type: () -> str
        return (
            '%s.%s(%s)' % (
                self.__module__,
                self.__class__.__name__.split('.')[-1],
                repr(str(self))
            )
        )

    def __iter__(self):
        # type: () -> Iterable[str]
        yield self.indicator_digit
        yield self.gcp
        yield self.item_reference
        yield self.check_digit


if __name__ == '__main__':
    import doctest
    doctest.testmod()
