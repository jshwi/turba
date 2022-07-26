"""
turba._main
===========

Contains package entry point.
"""
import shutil as _shutil

from ._core import AppFiles as _AppFiles
from ._core import Approved as _Approved
from ._core import Blacklist as _Blacklist
from ._core import Client as _Client
from ._core import Downloading as _Downloading
from ._core import Magnets as _Magnets
from ._core import Parser as _Parser
from ._core import Settings as _Settings

_HEADERS = {"User-Agent": "Mozilla/5.0"}


def main() -> None:
    """Main function for app.

    Scrape and collect magnets from provided URL.

    Check torrent dir for currently downloading torrents.

    Read and populate blacklist.

    Confirm with data collated which magnets the torrent client should
    be loaded with and add them to the client.

    Print torrent names that are now downloading.
    """
    parser = _Parser()
    if not _shutil.which("transmission-daemon"):
        raise RuntimeError("transmission-daemon is not installed")

    files = _AppFiles()

    # instantiate client with settings
    settings = _Settings(files.settings)
    client = _Client(**settings)

    # scrape magnets and evaluate torrents to load client with
    magnets = _Magnets(parser.args.url, _HEADERS)
    downloading = _Downloading(files.torrents)
    blacklist = _Blacklist(files.blacklist)
    approved = _Approved(magnets, downloading, blacklist)

    # load up approved torrents and announce
    if approved:
        client.add_torrents(*approved.values())
        print("the following unmatched torrents have just been added:")
        print("- {}".format("\n- ".join(approved.keys())))
