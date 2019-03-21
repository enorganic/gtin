"""
This module assembles a cross-reference used by *gtin.GTIN*
to determine the length of a GCP (GS1 Company Prefix).
"""

# Python 2 compatibility
from future.standard_library import install_aliases
install_aliases()

import os
import re
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


class GCPPrefixFormatList(object):
    """
    This class provides static methods for loading, retrieving, and parsing GCP prefix to GCP-length mappings
    """

    _prefixes_lengths = None

    @staticmethod
    def __getitem__(prefix):
        # type: (str) -> int
        if GCPPrefixFormatList._prefixes_lengths is None:
            GCPPrefixFormatList.load()
        return GCPPrefixFormatList._prefixes_lengths[prefix]

    @staticmethod
    def __contains__(prefix):
        # type: (str) -> int
        if(GCPPrefixFormatList._prefixes_lengths is None):
            GCPPrefixFormatList.load()
        return prefix in GCPPrefixFormatList._prefixes_lengths

    @staticmethod
    def load():
        # type: (...) -> None
        """
        Load the GCP prefixes from file
        """
        GCPPrefixFormatList._prefixes_lengths = {}
        with open(GCP_PREFIX_FORMAT_LIST_PATH, mode='r', encoding='utf-8', errors='ignore') as prefix_file:
            tree = ElementTree.fromstring(  # type: Element
                prefix_file.read()
            )
            for entry in (  # type: Element
                e for e in tree
                if (
                    ('prefix' in e.attrib) and
                    ('gcpLength' in e.attrib)
                )
            ):
                GCPPrefixFormatList._prefixes_lengths[
                    entry.attrib['prefix']
                ] = int(
                    entry.attrib['gcpLength']
                )

    @staticmethod
    def refresh():
        # type: (...) -> None
        try:
            with urlopen(GCP_PREFIX_FORMAT_LIST_URL) as response:
                data = response.read()
                if isinstance(data, bytes):
                    data = re.sub(
                        r'[\r\n][\r\n]+',
                        r'\n',
                        str(
                            data,
                            encoding='utf-8',
                            errors='ignore'
                        )
                    )
        except (HTTPError, URLError, TimeoutError) as error:
            updated = datetime.fromtimestamp(os.path.getmtime(
                GCP_PREFIX_FORMAT_LIST_PATH
            )).date()  # type: date
            type(error)(
                (
                    'The GCP prefix list could not be retrieved from "%(url)s". ' +
                    'A cached copy of this file, last updated on %(updated)s, will be used instead.\n\n'
                ) % dict(
                    url=GCP_PREFIX_FORMAT_LIST_URL,
                    updated=str(updated)
                ) + str(error)
            )
        if data:
            with open(GCP_PREFIX_FORMAT_LIST_PATH, mode='w') as prefix_file:
                prefix_file.write(data)


GCP_PREFIXES = GCPPrefixFormatList()
