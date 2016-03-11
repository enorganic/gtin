"""
Type declarations for use with Python 3.5+.
"""
import functools
from typing import Dict, IO, Optional
from xml.etree.ElementTree import Element
from datetime import date

GCP_PREFIX_FORMAT_LIST_URL = ''  # type: str
GCP_PREFIX_FORMAT_LIST_PATH = ''  # type: str


@functools.lru_cache()
def prefixes_lengths(local: bool=False) -> Dict:
    pl = {}  # type: Dict[int]
    gcp_prefix_format_list = None  # type: Optional[IO]
    local_gcp_prefix_format_list = None  # type: Optional[IO]
    updated = date.today()  # type: date
    tree = Element('GCPPrefixFormatList')  # type: Element
    e = Element('entry')  # type: Element
    return {}

