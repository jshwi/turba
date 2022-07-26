"""
tests
=====

Test package for ``turba``.
"""
# pylint: disable=too-few-public-methods
from __future__ import annotations

import json
import typing as t
from io import StringIO

from transmission_rpc import Session

# noinspection PyProtectedMember
from turba._core import Client

URL = "https://path/to/torrents"
URL_PAGE = "https://path/to/torrents/s/page/0/?q=some%20tv%20show"
INIT_SETTINGS_JSON = "init_settings_json"
INSTALL_TRANSMISSION_DAEMON = "install_transmission_daemon"
CLIENT_PATH = "turba._main._Client"
USER_DOWNLOADS = "/home/user/Downloads"
SETTINGS_JSON = json.dumps(
    {
        "alt-speed-down": 50,
        "alt-speed-enabled": False,
        "alt-speed-time-begin": 540,
        "alt-speed-time-day": 127,
        "alt-speed-time-enabled": False,
        "alt-speed-time-end": 1020,
        "alt-speed-up": 50,
        "bind-address-ipv4": "0.0.0.0",
        "bind-address-ipv6": "::",
        "blocklist-enabled": False,
        "blocklist-updates-enabled": True,
        "blocklist-url": "https://www.example.com/blocklist",
        "cache-size-mb": 4,
        "compact-view": False,
        "details-window-height": 572,
        "details-window-width": 700,
        "dht-enabled": True,
        "download-dir": USER_DOWNLOADS,
        "download-queue-enabled": True,
        "download-queue-size": 5,
        "encryption": 1,
        "idle-seeding-limit": 30,
        "idle-seeding-limit-enabled": False,
        "incomplete-dir": USER_DOWNLOADS,
        "incomplete-dir-enabled": False,
        "inhibit-desktop-hibernation": False,
        "lpd-enabled": False,
        "main-window-height": 500,
        "main-window-is-maximized": 0,
        "main-window-width": 786,
        "main-window-x": 453,
        "main-window-y": 300,
        "message-level": 2,
        "open-dialog-dir": "/home/user",
        "peer-congestion-algorithm": "",
        "peer-id-ttl-hours": 6,
        "peer-limit-global": 200,
        "peer-limit-per-torrent": 50,
        "peer-port": 51413,
        "peer-port-random-high": 65535,
        "peer-port-random-low": 49152,
        "peer-port-random-on-start": False,
        "peer-socket-tos": "default",
        "pex-enabled": True,
        "port-forwarding-enabled": True,
        "preallocation": 1,
        "prefetch-enabled": True,
        "queue-stalled-enabled": True,
        "queue-stalled-minutes": 30,
        "ratio-limit": 2,
        "ratio-limit-enabled": False,
        "recent-download-dir-1": USER_DOWNLOADS,
        "rename-partial-files": True,
        "rpc-authentication-required": False,
        "rpc-bind-address": "0.0.0.0",
        "rpc-enabled": False,
        "rpc-host-whitelist": "fedora",
        "rpc-host-whitelist-enabled": True,
        "rpc-password": "{34a1e5ff94042278aff8239dc7cf063adc173e73Egd82iWy",
        "rpc-port": 9091,
        "rpc-url": "/transmission/",
        "rpc-username": "",
        "rpc-whitelist": "127.0.0.1,::1",
        "rpc-whitelist-enabled": True,
        "scrape-paused-torrents-enabled": True,
        "script-torrent-done-enabled": False,
        "script-torrent-done-filename": "",
        "seed-queue-enabled": False,
        "seed-queue-size": 10,
        "show-backup-trackers": False,
        "show-extra-peer-details": False,
        "show-filterbar": True,
        "show-notification-area-icon": True,
        "show-options-window": True,
        "show-statusbar": True,
        "show-toolbar": True,
        "show-tracker-scrapes": False,
        "sort-mode": "sort-by-name",
        "sort-reversed": False,
        "speed-limit-down": 100,
        "speed-limit-down-enabled": False,
        "speed-limit-up": 100,
        "speed-limit-up-enabled": False,
        "start-added-torrents": True,
        "statusbar-stats": "total-ratio",
        "torrent-added-notification-enabled": True,
        "torrent-complete-notification-enabled": True,
        "torrent-complete-sound-command": (
            "canberra-gtk-play"
            " -i complete-download"
            " -d 'transmission torrent downloaded'"
        ),
        "torrent-complete-sound-enabled": True,
        "trash-can-enabled": True,
        "trash-original-torrent-files": False,
        "umask": 18,
        "upload-slots-per-torrent": 14,
        "user-has-given-informed-consent": True,
        "utp-enabled": True,
        "watch-dir": USER_DOWNLOADS,
        "watch-dir-enabled": False,
    }
)
ANNOUNCE_LIST = b"announce-list"
DISPLAY_NAME = b"display-name"
MAGNET_INFO = b"magnet-info"
DEFAULT_ANNOUNCE_LIST = [[b"udp://tracker.torrenttrackerhere.com:80"]]


class Torrent(t.NamedTuple):
    """Torrent attributes."""

    name: str
    filename: str
    magnet: str
    bencode: t.Dict[bytes, t.List[t.List[bytes]] | t.Dict[bytes, bytes]]


TORRENTS = (
    Torrent(
        "Popular_tv_Show_Season_1_720p_BluRay_x264",
        "7b8a6e777e5f7bf514f73007ee638135f6daa540.torrent",
        (
            "magnet:?"
            "xt=urn:btih:7b8a6e777e5f7bf514f73007ee638135f6daa540&"
            "dn=Popular_tv_Show_Season_1_720p_BluRay_x264&"
            "tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&"
        ),
        {
            ANNOUNCE_LIST: DEFAULT_ANNOUNCE_LIST,
            MAGNET_INFO: {
                DISPLAY_NAME: b"Popular_tv_Show_Season_1_720p_BluRay_x264",
                b"info_hash": (
                    b"{\x8anw~_{\xf5\x14\xf70\x07\xeec\x815\xf6\xda\xa5@"
                ),
            },
        },
    ),
    Torrent(
        "Popular_tv_Show_Season_2_720p_BluRay_x264",
        "cc809f86f50e8429767ba6396e20d5aa2f482e78.torrent",
        (
            "magnet:?"
            "xt=urn:btih:cc809f86f50e8429767ba6396e20d5aa2f482e78&"
            "dn=Popular_tv_Show_Season_2_720p_BluRay_x264&"
            "tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&"
        ),
        {
            ANNOUNCE_LIST: DEFAULT_ANNOUNCE_LIST,
            MAGNET_INFO: {
                DISPLAY_NAME: b"Popular_tv_Show_Season_2_720p_BluRay_x264",
                b"info_hash": (
                    b"\xcc\x80\x9f\x86\xf5\x0e\x84)v{\xa69n \xd5\xaa/H.x"
                ),
            },
        },
    ),
    Torrent(
        "Popular_tv_Show_Season_3_720p_BluRay_x264",
        "bec925ce223a0728b7e8a81634ab91a6e428878c.torrent",
        (
            "magnet:?"
            "xt=urn:btih:bec925ce223a0728b7e8a81634ab91a6e428878c&"
            "dn=Popular_tv_Show_Season_3_720p_BluRay_x264&"
            "tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&"
        ),
        {
            ANNOUNCE_LIST: DEFAULT_ANNOUNCE_LIST,
            MAGNET_INFO: {
                DISPLAY_NAME: b"Popular_tv_Show_Season_3_720p_BluRay_x264",
                b"info_hash": (
                    b'\xbe\xc9%\xce":\x07(\xb7\xe8\xa8\x164\xab\x91\xa6\xe4('
                    b"\x87\x8c"
                ),
            },
        },
    ),
)
HTML = f"""
<!DOCTYPE html>
<html lang="en">
<head><title>Torrent Site - Get torrents here</title></head>
<body>
<h2><span>Search results: popular tv show</span></h2>
<div>
  <div id="content">
    <div id="main-content">
    <table id="searchResult">
      <thead id="tableHead">
      <tr class="header">
        <td>
          <div class="detName">
            <a href="https://">{TORRENTS[0].name}</a>
          </div>
          <a href="{TORRENTS[0].magnet}"
            title="Download this torrent using magnet">
            <img src="" alt="Magnet link"></a>
        </td>
        <td>
          <div class="detName">
            <a href="https://">{TORRENTS[1].name}</a>
          </div>
          <a href="{TORRENTS[1].magnet}"
            title="Download this torrent using magnet">
            <img src="" alt="Magnet link"></a>
        </td>
        <td>
          <div class="detName">
            <a href="https://">{TORRENTS[2].name}</a>
          </div>
          <a href="{TORRENTS[2].magnet}"
            title="Download this torrent using magnet">
            <img src="" alt="Magnet link"></a>
        </td>
      </tr>
    </table>
  </div>
  </div>
</div>
</body>
</html>
"""


MockMainFixture = t.Callable[..., None]


class MockUrlOpen:
    """Mock URL open."""

    def __init__(self, _: str) -> None:
        """Nothing to do."""

    def __enter__(self):
        return StringIO(HTML)

    def __exit__(self, _: t.Any, __: t.Any, ___: t.Any) -> None:
        """Nothing to do."""


class MockClient(Client):
    """Mock RPC client."""

    def __init__(self, *_: t.Any, **__: t.Any) -> None:
        super().__init__()
        self.added_torrents: t.List[str] = []

    def get_session(self, timeout: float = None) -> Session:
        """Prevent actual session requests."""

    def add_torrent(  # pylint: disable=arguments-differ
        self, magnet: str, **_: t.Any
    ) -> None:
        """Mock ``add_torrent`` to only collect torrents added.

        :param magnet: Torrent magnet.
        """
        self.added_torrents.append(magnet)
