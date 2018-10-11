"""
This module assembles a cross-reference used by *gtin.GTIN*
to determine the length of a GCP (GS1 Company Prefix).
"""

# Python 2 compatibility
from future.standard_library import install_aliases
install_aliases()

import os
import functools
import re
import warnings
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from datetime import datetime
from xml.etree import ElementTree


GCP_PREFIX_FORMAT_LIST_URL = 'https://www.gs1.org/docs/gcp_length/gcpprefixformatlist.xml'  # type: str
GCP_PREFIX_FORMAT_LIST_PATH = os.path.join(  # type: str
    os.path.dirname(
        os.path.abspath(
            __file__
        )
    ),
    'GCPPrefixFormatList.xml'
)


@functools.lru_cache(maxsize=1)
def prefixes_lengths(local=False):
    # type: (bool) -> Dict
    """
    This function provides a current mapping of GS1 prefixes to the length
    of GTIN Company Prefixes beginning with each prefix. Note: The "prefix"
    of a GCP starts at the second digit of a GTIN-14, because the
    first digit indicates the logistic unit level ("0" indicates a consumer-level
    unit).

    :param local:

        If *True*, a local, cached GCP prefix format list will be used instead of checking for an
        updated copy online.
    """
    pl = {}  # type: Optional[Dict[str, int]]
    gcp_prefix_format_list = None  # type: Optional[IO]
    if not local:
        try:
            with urlopen(GCP_PREFIX_FORMAT_LIST_URL) as r:
                gcp_prefix_format_list = r.read()
                if isinstance(gcp_prefix_format_list, bytes):
                    gcp_prefix_format_list = re.sub(
                        r'[\r\n][\r\n]+',
                        r'\n',
                        str(
                            gcp_prefix_format_list,
                            encoding='utf-8',
                            errors='ignore'
                        )
                    )
        except (HTTPError, URLError, TimeoutError):
            updated = datetime.fromtimestamp(os.path.getmtime(
                GCP_PREFIX_FORMAT_LIST_PATH
            )).date()  # type: date
            warnings.warn(
                (
                    'The GCP prefix list could not be retrieved from "%(url)s". ' +
                    'A cached copy of this file, last updated on %(updated)s, will be used instead.'
                ) % dict(
                    url=GCP_PREFIX_FORMAT_LIST_URL,
                    updated=str(updated)
                )
            )
    with open(GCP_PREFIX_FORMAT_LIST_PATH, mode='r', encoding='utf-8', errors='ignore') as f:
        local_gcp_prefix_format_list = f.read()
    if gcp_prefix_format_list is None:
        gcp_prefix_format_list = local_gcp_prefix_format_list
    else:
        if local_gcp_prefix_format_list != gcp_prefix_format_list:
            with open(GCP_PREFIX_FORMAT_LIST_PATH, mode='w') as f:
                f.write(gcp_prefix_format_list)
    tree = ElementTree.fromstring(  # type: Element
        gcp_prefix_format_list
    )
    for entry in (  # type: Element
        e for e in tree
        if (
            ('prefix' in e.attrib) and
            ('gcpLength' in e.attrib)
        )
    ):
        pl[
            entry.attrib['prefix']
        ] = int(
            entry.attrib['gcpLength']
        )
    return pl


if __name__ == "__main__":
    prefixes_lengths()
    import doctest
    doctest.testmod()
