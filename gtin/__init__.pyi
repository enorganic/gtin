from builtins import int, str
from numbers import Number, Real
from typing import Union, Optional, Iterable
import functools


class GTIN:

    def __init__(
        self,
        gtin: Optional[Union[str,Real]]=None,
        length: Optional[Union[Real]]=None,
        raw: Optional[Union[str,Real]]=None,
        indicator_digit: Optional[Union[str,Real]]=None,
        gcp: Optional[str]=None,
        item_reference: Optional[Union[str,Real]]=None,
        check_digit: Optional[Union[str,Real]]=None
    ):
        class Data:
            raw = None # type: int
            length = None # type: int
        self.data = None # type: 'Data'

    def __len__(self) -> int:
        pass

    @property
    def length(self) -> int:
        return self.data.length

    @length.setter
    def length(self, l: int) -> None:
        pass

    @property
    def raw(self) -> int:
        pass

    @raw.setter
    def raw(self,value: Optional[Union[str,Number]]) -> None:
        pass

    @functools.lru_cache()
    def get_check_digit(self) -> Optional[str]:
        pass

    @property
    def check_digit(self) -> Optional[str]:
        pass

    @functools.lru_cache()
    def get_gcp(self) -> Optional[str]:
        pass

    @property
    def gcp(self) -> Optional[str]:
        pass

    @property
    def indicator_digit(self) -> str:
        pass

    @property
    def indicator_digit(self) -> str:
        pass

    @property
    def item_reference(self) -> str:
        pass

    def __int__(self) -> int:
        pass

    def __float__(self) -> float:
        pass

    @functools.lru_cache()
    def __str__(self) -> str:
        pass

    def __hash__(self) -> int:
        pass

    def __repr__(self) -> str:
        pass

    def __iter__(self) -> Iterable:
        pass
