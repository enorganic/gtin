"""
A library for parsing GTINs ("Global Trade Item Numbers"—also known as UPC/EAN/JAN/ISBN).

Author: David Belais <david@belais.me>
License: MIT
Documentation: http://gtin.readthedocs.org
"""

# Python 2 compatibility
from __future__ import division
from future.standard_library import install_aliases
install_aliases()
from future.utils import python_2_unicode_compatible
from builtins import int, bytes, str

import re
import functools
from numbers import Number
from gtin.gcp import prefixes_lengths as gcp_prefixes_lengths


class GTINError(Exception):
    pass


class GTINTypeError(GTINError, TypeError):
    pass


class CheckDigitError(GTINError, ValueError):
    pass


class IndicatorDigitError(GTINError, ValueError):
    pass


class GCPNotFoundError(GTINError, ValueError):
    pass


@python_2_unicode_compatible
class GTIN:
    """
    gtin
    ====

    A python package for parsing GTINs ("Global Trade Item Numbers"—also known as UPC/EAN/JAN/ISBN).

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

        - If no value is passed for *length*, and *gtin* is a *str*—*length* is inferred based on the character
          length of *gtin*.
        - If no value is passed for *length*, *gtin* is *None*, and *raw* is a *str*—*length* is inferred based
          on the length of *raw* (adding 1, to account for the absent check-digit).
        - If no length is passed, and none can be inferred from *gtin* or *raw*, *length* defaults to 14.

    :raw:

        A string or number representing the GTIN, excluding the check-digit.

        - If a value is provided for the parameter *gtin*, this parameter is not used, but is instead derived
          from *gtin*.

    In lieu of passing a complete GTIN, with or without the check-digit, using the above parameters—it is possible to
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
    ~~~~~~~~

    >>> from gtin import GTIN

    A *GTIN* initialized without any arguments:

    >>> print(repr(GTIN()))
    GTIN('00000000000000')

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
    """

    def __init__(
        self,
        gtin=None,  # type: Optional[Union[str, Real]] = None
        length=None,  # type: Optional[Union[Real]] = None
        raw=None,  # type: Optional[Union[str, Real]] = None
        indicator_digit=None,  # type: Optional[Union[str, Real]] = None
        gcp=None,  # type: Optional[str] = None
        item_reference=None,  # type: Optional[Union[str, Real]] = None
        check_digit=None  # type: Optional[Union[str, Real]] = None
    ):
        class Data:
            raw = None  # type: int
            length = None  # type: int

        self.data = Data  # type: "Data"
        if gtin is not None:
            if isinstance(gtin, self.__class__):
                raw = gtin.raw
                length = len(gtin)
            elif isinstance(gtin, (str, bytes)):
                if isinstance(gtin, bytes):
                    gtin = str(gtin, encoding='utf-8', errors='ignore')
                g = re.sub(r'[^\d]', '', gtin)
                if g == '':
                    raise GTINError(
                        '%s is not a valid GTIN. ' % repr(gtin) +
                        'A GTIN should contain 1 or more numeric digits.'
                    )
                gtin = g
                if length is None:
                    length = len(gtin)
                    if check_digit is not None:
                        length += 1
                if check_digit is None:
                    raw = int(gtin[:-1])
                    check_digit = gtin[-1]
                else:
                    raw = int(gtin)
            elif isinstance(gtin, Number) or hasattr(gtin, '__int__'):
                g = str(abs(int(gtin)))
                check_digit = g[-1]
                raw = int(g[:-1])
            else:
                raise GTINTypeError('The parameter `gtin` must be a `str` or `int`.')
        elif raw is not None:
            if isinstance(raw, (str, bytes)):
                if isinstance(raw, bytes):
                    raw = str(raw, encoding='utf-8', errors='ignore')
                raw = re.sub(r'[^\d]', '', raw)
                if length is None:
                    length = len(raw) + 1
                raw = abs(int(raw))
            elif isinstance(raw, Number) or hasattr(raw, '__int__'):
                raw = abs(int(raw))
            else:
                raise GTINTypeError('The parameter `raw` must be a `str` or `int`.')
        elif (
            (indicator_digit is not None) or
            (gcp is not None) or
            (item_reference is not None) or
            (check_digit is not None)
        ):
            if indicator_digit is None:
                indicator_digit = '0'
            else:
                if (
                        (length is not None) and
                        (length != 14)
                ):
                    raise IndicatorDigitError(
                        'An indicator digit only applies to GTIN-14.'
                    )
                if isinstance(indicator_digit, (str, bytes)):
                    if isinstance(indicator_digit, bytes):
                        indicator_digit = str(
                            indicator_digit,
                            encoding='utf-8',
                            errors='ignore'
                        )
                    indicator_digit = re.sub(r'[^\d]', '', indicator_digit)
                elif isinstance(indicator_digit, Number):
                    indicator_digit = str(abs(int(indicator_digit)))
                if len(indicator_digit) > 1:
                    raise IndicatorDigitError(
                        'The parameter `indicator_digit` must be a one-character `str` comprised of a numeric digit, ' +
                        'or an integer between 0 and 9.'
                    )
            if gcp is not None:
                if isinstance(gcp, (str, bytes)):
                    if isinstance(gcp, bytes):
                        gcp = str(
                            gcp,
                            encoding='utf-8',
                            errors='ignore'
                        )
                    gcp = re.sub(r'[^\d]', '', gcp)
                elif isinstance(gcp, Number):
                    gcp = str(abs(int(gcp)))
            if item_reference is not None:
                if isinstance(item_reference, (str, bytes)):
                    if isinstance(item_reference, bytes):
                        item_reference = str(
                            item_reference,
                            encoding='utf-8',
                            errors='ignore'
                        )
                    item_reference = re.sub(r'[^\d]', '', item_reference)
                elif isinstance(item_reference, Number):
                    item_reference = str(abs(int(item_reference)))
            if (
                (gcp is not None) and
                (item_reference is not None) and
                len(gcp) + len(item_reference) != 12
            ):
                raise GTINTypeError(
                    'The character length of parameters `gcp` and `item_reference` combined must equal 12.'
                )
            elif gcp is None:
                gcp = '0' * (12 - len(item_reference))
            elif item_reference is None:
                item_reference = '0' * (12 - len(gcp))
            raw = int(
                indicator_digit +
                gcp +
                item_reference
            )
        else:
            raw = 0
        if length is None:
            length = 14
        self.length = length
        self.raw = raw
        if check_digit is not None:
            cd = self.check_digit
            if check_digit != cd:
                raise CheckDigitError(
                    ('This GTIN ("%s") has an invalid check-digit ("%s"). ' % (gtin, check_digit)) +
                    ('The correct check-digit would be "%s".' % cd)
                )

    def __len__(self):
        # type: () -> int
        return self.length

    @property
    def length(self):
        # type: () -> int
        return self.data.length

    @length.setter
    def length(self, l):
        # type: (int) -> None
        self.__str__.cache_clear()
        self.data.length = abs(int(l))

    @property
    def raw(self):
        # type: () -> int
        return self.data.raw

    @raw.setter
    def raw(self, value):
        # type: (Union[str, Number]) -> None
        self.__str__.cache_clear()
        self.get_check_digit.cache_clear()
        self.get_gcp.cache_clear()
        if value is None:
            self.data.raw = None
        else:
            if isinstance(value, (str, bytes)):
                if isinstance(value, bytes):
                    value = str(
                        value,
                        encoding='utf-8',
                        errors='ignore'
                    )
                value = re.sub(r'[^\d]', '', value)
                self.length = len(value) + 1
            self.data.raw = abs(int(value))
            integer_string = str(self.data.raw)
            length = len(self)
            if length <= len(integer_string):
                raise ValueError(
                    ('The value %s for raw has too many ' % repr(self.data.raw)) +
                    ('digits for a GTIN with a length of %s.' % str(length))
                )

    @functools.lru_cache(maxsize=None)
    def get_check_digit(self):
        # type: () -> Optional[str]
        r = self.raw
        if r is None:
            return None
        digits = tuple(d for d in reversed(str(r)))
        return str(
            10 - (
                (
                    (sum(int(d) for d in digits[::2]) * 3) +
                    (sum(int(d) for d in digits[1::2]))
                ) % 10
            )
        )[-1]

    @property
    def check_digit(self):
        # type: () -> Optional[str]
        return self.get_check_digit()

    @functools.lru_cache(maxsize=None)
    def get_gcp(self):
        # type: () -> Optional[str]
        gp_l = gcp_prefixes_lengths()
        prefixes = set(gp_l.keys())
        g = str(self)
        if len(g) < 14:
            g = ('0' * (14 - len(g))) + g
        p = g[1:-1]
        l = None
        while p:
            if p in prefixes:
                l = gp_l[p]
                break
            else:
                p = p[:-1]
        if l is None:
            raise GCPNotFoundError(
                'No GCP could be found matching this GTIN: %s' % g
            )
        else:
            return g[1:1 + l] if l else ''

    @property
    def gcp(self):
        # type: () -> Optional[str]
        return self.get_gcp()

    @property
    def indicator_digit(self):
        # type: () -> Optional[str]
        return str(self)[0]

    @property
    def indicator_digit(self):
        # type: () -> Optional[str]
        return str(self)[0]

    @property
    def item_reference(self):
        # type: () -> Optional[str]
        return str(self)[len(self.gcp) + 1:-1]

    def __int__(self):
        # type: () -> int
        return int(str(self))

    def __float__(self):
        # type: () -> float
        return float(str(self))

    @functools.lru_cache(maxsize=None)
    def __str__(self):
        # type: () -> str
        if self.raw is None:
            return '0' * self.length
        g = str(self.raw) + self.check_digit
        return (
            ('0' * (self.length - len(g))) +
            g
        )

    def __hash__(self):
        # type: () -> int
        return self.raw or 0

    def __repr__(self):
        # type: () -> str
        return (
            '%s(%s)' % (
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
