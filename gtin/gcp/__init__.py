"""
This module assembles a cross-reference used by *gtin.GTIN*
to determine the length of a GCP (GS1 Company Prefix).
"""

# Python 2 compatibility
from future.standard_library import install_aliases
install_aliases()

import os
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from datetime import datetime, timedelta
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
    This class provides methods for loading, retrieving, and parsing GCP prefix-to-length mappings
    """

    _prefixes_lengths = None
    _modified = None

    @classmethod
    def __getitem__(cls, prefix):
        # type: (str) -> int
        if cls._prefixes_lengths is None:
            cls.load()
        return cls._prefixes_lengths[prefix]

    @classmethod
    def __contains__(cls, prefix):
        # type: (str) -> int
        if(cls._prefixes_lengths is None):
            cls.load()
        return prefix in cls._prefixes_lengths

    @classmethod
    def modified(cls):
        if cls._modified is None:
            cls._modified = datetime.fromtimestamp(os.path.getmtime(
                GCP_PREFIX_FORMAT_LIST_PATH
            ))
        return cls._modified

    @classmethod
    def load(cls):
        # type: (...) -> None
        """
        Load GCP prefixes XML
        """

        # Check for updates every 30 days
        if cls.modified() < datetime.now() - timedelta(days=30):
            cls.refresh()

        cls._prefixes_lengths = {}

        with open(GCP_PREFIX_FORMAT_LIST_PATH, mode='r') as prefix_file:
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
                cls._prefixes_lengths[
                    entry.attrib['prefix']
                ] = int(
                    entry.attrib['gcpLength']
                )

    @classmethod
    def refresh(cls):
        # type: (...) -> None
        """
        Retrieve and updated XML mapping
        """
        try:
            with urlopen(GCP_PREFIX_FORMAT_LIST_URL) as response:
                data = response.read()
                if not isinstance(data, str):
                    data = str(
                        data,
                        encoding='utf-8',
                        errors='ignore'
                    )
        except (HTTPError, URLError, OSError) as error:
            type(error)(
                (
                    'The GCP prefix list could not be retrieved from "%(url)s". ' +
                    'A cached copy of this file, last updated on %(updated)s, will be used instead.\n\n'
                ) % dict(
                    url=GCP_PREFIX_FORMAT_LIST_URL,
                    updated=str(cls.modified().date())
                ) + str(error)
            )
        if data:
            with open(GCP_PREFIX_FORMAT_LIST_PATH, mode='w') as prefix_file:
                prefix_file.write(data)
            cls._modified = datetime.now()


GCP_PREFIXES = GCPPrefixFormatList()
