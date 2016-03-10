"""
Type declarations for use with Python 3.5+.
"""

from numbers import Number, Real
from typing import Union, Optional, Iterable
import functools


class GTIN:
    def __init__(
        self,
        gtin: Optional[Union[str, Real]] = None,
        length: Optional[Union[Real]] = None,
        raw: Optional[Union[str, Real]] = None,
        indicator_digit: Optional[Union[str, Real]] = None,
        gcp: Optional[str] = None,
        item_reference: Optional[Union[str, Real]] = None,
        check_digit: Optional[Union[str, Real]] = None
    ):
        class Data:
            raw = 0  # type: int
            length = 0  # type: int

        self.data = Data()  # type: 'Data'

    def __len__(self) -> int:
        return 0

    @property
    def length(self) -> int:
        return 0

    @length.setter
    def length(self, l: int) -> None:
        pass

    @property
    def raw(self) -> int:
        return 0

    @raw.setter
    def raw(self, value: Union[str, Number]) -> None:
        pass

    @functools.lru_cache()
    def get_check_digit(self) -> str:
        return '0'

    @property
    def check_digit(self) -> str:
        return '0'

    @functools.lru_cache()
    def get_gcp(self) -> Optional[str]:
        return None

    @property
    def gcp(self) -> Optional[str]:
        return None

    @property
    def indicator_digit(self) -> str:
        return ''

    @property
    def indicator_digit(self) -> str:
        return ''

    @property
    def item_reference(self) -> str:
        return ''

    def __int__(self) -> int:
        return 0

    def __float__(self) -> float:
        return 0.0

    @functools.lru_cache()
    def __str__(self) -> str:
        return ''

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> str:
        return ''

    def __iter__(self) -> Iterable[str]:
        yield ''
