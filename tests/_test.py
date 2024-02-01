"""
tests._test
===========
"""

# pylint: disable=too-many-arguments,protected-access,too-few-public-methods
import typing as t
from pathlib import Path

import appdirs
import pytest

import turba

from . import (
    CLIENT_PATH,
    INIT_SETTINGS_JSON,
    INSTALL_TRANSMISSION_DAEMON,
    TORRENTS,
    URL,
    MockClient,
    MockMainFixture,
)


def test_version(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test ``turba.__version__``.

    :param monkeypatch: Mock patch environment and attributes.
    """
    version = "0.1.0"
    monkeypatch.setattr("turba.__version__", version)
    assert turba.__version__ == version


def test_mutable_sequence() -> None:
    """Get coverage on ``MutableSequence``."""
    # noinspection PyUnresolvedReferences
    seq: t.MutableSequence = turba._objects.MutableSequence()
    value = "value"
    seq.append(value)
    assert value in seq
    assert len(seq) == 1
    other_value = "other-value"
    seq[0] = other_value
    seq.pop()
    assert other_value not in seq


def test_mutable_mapping() -> None:
    """Get coverage on ``MutableMapping``."""
    # noinspection PyUnresolvedReferences
    mapping: t.MutableMapping = turba._objects.MutableMapping()
    assert len(mapping) == 0
    mapping[1] = 1
    assert 1 in mapping
    assert mapping[1] == 1
    assert len(mapping) == 1
    del mapping[1]
    assert len(mapping) == 0


def test_no_transmission_daemon(main: MockMainFixture) -> None:
    """Test error raised when ``transmission-daemon`` not installed.

    :param main: Mock package entry point.
    """
    with pytest.raises(RuntimeError) as err:
        main(URL)

    assert "transmission-daemon is not installed" in str(err.value)


@pytest.mark.usefixtures(INIT_SETTINGS_JSON, INSTALL_TRANSMISSION_DAEMON)
def test_basic(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    main: MockMainFixture,
) -> None:
    """Test basic process when URL is provided.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys output.
    :param main: Mock package entry point.
    """
    mock_client = MockClient()
    monkeypatch.setattr(CLIENT_PATH, lambda *_, **__: mock_client)
    main(URL)
    out = capsys.readouterr()[0]
    assert "the following unmatched torrents have just been added:" in out
    assert TORRENTS[0].name in out
    assert TORRENTS[1].name in out
    assert TORRENTS[2].name in out
    assert TORRENTS[0].magnet in mock_client.added_torrents
    assert TORRENTS[1].magnet in mock_client.added_torrents
    assert TORRENTS[2].magnet in mock_client.added_torrents


@pytest.mark.usefixtures(INIT_SETTINGS_JSON, INSTALL_TRANSMISSION_DAEMON)
@pytest.mark.parametrize("downloading", [0, 1, 2])
def test_already_downloading(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    main: MockMainFixture,
    downloading: int,
) -> None:
    """Test process when a torrent collected is already downloading.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys output.
    :param main: Mock package entry point.
    :param downloading: Index downloading.
    """
    not_downloading = [i for i in range(len(TORRENTS)) if i != downloading]
    torrent = (
        Path(appdirs.user_config_dir())
        / "transmission-daemon"
        / "torrents"
        / TORRENTS[downloading].filename
    )
    torrent.parent.mkdir(parents=True)
    torrent.touch()
    mock_client = MockClient()
    monkeypatch.setattr(CLIENT_PATH, lambda *_, **__: mock_client)
    monkeypatch.setattr(
        "turba._core._bencodepy.decode",
        lambda x: TORRENTS[downloading].bencode,
    )
    main(URL)
    out = capsys.readouterr()[0]
    assert TORRENTS[downloading].name not in out
    assert all(TORRENTS[i].name in out for i in not_downloading)
    assert TORRENTS[downloading].magnet not in mock_client.added_torrents
    assert all(
        TORRENTS[i].magnet in mock_client.added_torrents
        for i in not_downloading
    )


@pytest.mark.usefixtures(INIT_SETTINGS_JSON, INSTALL_TRANSMISSION_DAEMON)
@pytest.mark.parametrize("blacklisted", [0, 1, 2])
def test_blacklisted(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    main: MockMainFixture,
    blacklisted: int,
) -> None:
    """Test process when a torrent collected is blacklisted.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys output.
    :param main: Mock package entry point.
    :param blacklisted: Index to blacklist.
    """
    not_blacklisted = [i for i in range(len(TORRENTS)) if i != blacklisted]
    mock_client = MockClient()
    blacklist = Path(appdirs.user_config_dir(turba.__name__)) / "blacklist"
    blacklist.parent.mkdir(parents=True)
    blacklist.write_text(TORRENTS[blacklisted].name)
    monkeypatch.setattr(CLIENT_PATH, lambda *_, **__: mock_client)
    main(URL)
    out = capsys.readouterr()[0]
    assert TORRENTS[blacklisted].name not in out
    assert all(TORRENTS[i].name in out for i in not_blacklisted)
    assert TORRENTS[blacklisted].magnet not in mock_client.added_torrents
    assert all(
        TORRENTS[i].magnet in mock_client.added_torrents
        for i in not_blacklisted
    )
