"""
turba._core
===========
"""
from __future__ import annotations

import json as _json
import typing as _t
from argparse import ArgumentParser as _ArgumentParser
from pathlib import Path as _Path
from urllib.request import Request as _Request
from urllib.request import urlopen as _urlopen

import bencodepy as _bencodepy
from appdirs import AppDirs as _AppDirs
from bs4 import BeautifulSoup as _BeautifulSoup
from object_colors import Color as _Color
from transmission_rpc import Client as _Client

from ._objects import MutableMapping as _MutableMapping
from ._objects import MutableSequence as _MutableSequence

color = _Color()

color.populate_colors()

NAME = __name__.split(".", maxsplit=1)[0]


class Parser(_ArgumentParser):
    """The app's commandline parser."""

    def __init__(self) -> None:
        super().__init__(prog=color.cyan.get(NAME))
        self._add_arguments()
        self.args = self.parse_args()

    def _add_arguments(self) -> None:
        self.add_argument(
            "url", metavar="URL", action="store", help="url to harvest"
        )


class AppDirs(_AppDirs):
    """Directories for app to interact with.

    Create app's data dirs on instantiation.
    """

    def __init__(self) -> None:
        super().__init__(appname=NAME)
        self.user_config_dir.mkdir(exist_ok=True, parents=True)

    @property
    def user_config_dir(self) -> _Path:
        """Path to the user's config dir."""
        return _Path(super().user_config_dir)

    @property
    def user_client_dir(self) -> _Path:
        """Path to the ``transmission-daemon`` config dir."""
        return self.user_config_dir.parent / "transmission-daemon"

    @property
    def torrents(self) -> _Path:
        """Path to the ``transmission-daemon`` torrent dir."""
        return self.user_client_dir / "torrents"


class AppFiles(AppDirs):
    """Files for app to interact with."""

    @property
    def blacklist(self) -> _Path:
        """Path to the blacklist file."""
        return self.user_config_dir / "blacklist"

    @property
    def settings(self) -> _Path:
        """Path to the ``transmission-daemon`` settings file."""
        return self.user_client_dir / "settings.json"


class Blacklist(_MutableSequence[str]):
    """Read and collect session's blacklisted torrents for file.

    :param path: Path to blacklist config.
    """

    def __init__(self, path: _Path) -> None:
        super().__init__()
        if path.is_file():
            self.extend(path.read_text().splitlines())


class Downloading(_MutableSequence[str]):
    """Read, decode, and collect downloading .torrent files.

    :param path: Path to torrents dir.
    """

    def __init__(self, path: _Path) -> None:
        super().__init__()
        if path.is_dir():
            for file in path.iterdir():
                obj = _bencodepy.decode(file.read_bytes())
                result = obj.get(b"magnet-info", {}).get(b"display-name")
                if result is not None:
                    self.append(result.decode())


class Magnets(_MutableMapping[str, str]):
    """Scrape URl and collect named magnet links.

    :param url: URL to scrape.
    :param headers: Request headers.
    """

    def __init__(self, url: str, headers: _t.Dict[str, str]) -> None:
        super().__init__()
        request = _Request(url, headers=headers)
        with _urlopen(request) as webio:
            soup = _BeautifulSoup(webio.read(), "html.parser")
            for anchor in soup("a"):
                href = anchor.get("href")
                if href is not None and href.startswith("magnet"):
                    self[href.split("dn=")[-1].split("&")[0]] = href


class Settings(_MutableMapping[str, _t.Union[int, str]]):
    """Client's settings parsed from json config.

    :param path: Path to client's settings json file.
    """

    def __init__(self, path: _Path) -> None:
        super().__init__()
        settings = _json.loads(path.read_text())
        self.update(
            dict(
                host=settings["rpc-host-whitelist"],
                port=settings["rpc-port"],
                username=settings["rpc-username"],
                password=settings["rpc-password"],
                path=f"{settings['rpc-url']}/rpc",
            )
        )


class Approved(_MutableMapping[str, str]):
    """Analyze data sequences for approved torrents.

    :param magnets: Instantiated ``Magnets`` object.
    :param args: Sequence of magnets to ignore.
    """

    def __init__(
        self, magnets: Magnets, *args: Blacklist | Downloading
    ) -> None:
        super().__init__()
        exclusions = {i for v in args for i in v}
        for name, magnet in magnets.items():
            if name not in exclusions:
                self[name] = magnet


class Client(_Client):
    """Torrent client class."""

    def add_torrents(self, *args: str) -> None:
        """Add torrent to transfers list:

        :param args: Torrents to add.
        """
        for magnet in args:
            self.add_torrent(magnet)
