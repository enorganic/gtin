"""
This is a script to update the GCP Prefix Format List for the `gtin` project,
and set the project bugfix version based on the date the list was last updated.
"""
import os
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from http.client import HTTPResponse
from typing import IO, Tuple
from configparser import ConfigParser
from iso8601 import parse_date  # type: ignore
from gtin import read_gcp_prefix_format_list

PROJECT_DIRECTORY: str = urljoin(os.path.abspath(__file__), "../")
GCP_PREFIX_FORMAT_LIST_URL: str = (
    "https://www.gs1.org/docs/gcp_length/gcpprefixformatlist.xml"
)
GCP_PREFIX_FORMAT_LIST_PATH: str = (
    f"{PROJECT_DIRECTORY}gtin/GCPPrefixFormatList.xml"
)


def update_version() -> None:
    setup_cfg_path: str = f"{PROJECT_DIRECTORY}setup.cfg"
    parser: ConfigParser = ConfigParser()
    parser.read(setup_cfg_path)
    old_version: str = parser["metadata"]["version"]
    version_tuple: Tuple[str, ...] = tuple(old_version.split(".")[:2])
    # The last number ("bugfix" number) in the version is the number of seconds
    # since the epoch on the date the GCP Prefix Format List was last updated
    version_tuple += (("0",) * (len(version_tuple) - 3)) + (
        str(
            int(
                parse_date(
                    read_gcp_prefix_format_list().attrib["date"]
                ).timestamp()
            )
        ),
    )
    new_version: str = ".".join(version_tuple)
    print(
        f"Updating the project version from {repr(old_version)} to "
        f"{repr(new_version)}"
    )
    parser["metadata"]["version"] = new_version
    setup_cfg_io: IO[str]
    with open(setup_cfg_path, "w") as setup_cfg_io:
        parser.write(setup_cfg_io)


def download_gcp_prefix_format_list() -> None:
    print(
        f"Downloading {GCP_PREFIX_FORMAT_LIST_URL} "
        f"to {GCP_PREFIX_FORMAT_LIST_PATH}"
    )
    response: HTTPResponse
    request: Request = Request(
        GCP_PREFIX_FORMAT_LIST_URL, headers={"User-agent": ""}
    )
    os.makedirs(os.path.dirname(GCP_PREFIX_FORMAT_LIST_PATH), exist_ok=True)
    with urlopen(request) as response:
        data: str = str(response.read(), encoding="utf-8", errors="ignore")
    file_io: IO[str]
    with open(GCP_PREFIX_FORMAT_LIST_PATH, "w") as file_io:
        file_io.write(data)


def main() -> None:
    download_gcp_prefix_format_list()
    update_version()


if __name__ == "__main__":
    main()
