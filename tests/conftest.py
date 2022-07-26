"""
tests.conftest
==============
"""
from pathlib import Path

import pytest

import turba

from . import (
    CLIENT_PATH,
    INIT_SETTINGS_JSON,
    INSTALL_TRANSMISSION_DAEMON,
    SETTINGS_JSON,
    MockClient,
    MockMainFixture,
    MockUrlOpen,
)


@pytest.fixture(name="env", autouse=True)
def fixture_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up environment for testing.

    :param tmp_path: Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    """
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / ".config"))
    monkeypatch.setattr(CLIENT_PATH, MockClient)
    monkeypatch.setattr("shutil.which", lambda x: None)
    monkeypatch.setattr("turba._core._urlopen", MockUrlOpen)
    monkeypatch.setattr(
        "os.path.expanduser", lambda x: x.replace("~", str(tmp_path))
    )


@pytest.fixture(name=INIT_SETTINGS_JSON)
def fixture_init_settings_json(tmp_path: Path) -> None:
    """Create test ``transmission-daemon`` settings file.

    :param tmp_path: Create and return temporary directory.
    """
    settings = tmp_path / ".config" / "transmission-daemon" / "settings.json"
    settings.parent.mkdir(parents=True)
    settings.write_text(SETTINGS_JSON)


@pytest.fixture(name=INSTALL_TRANSMISSION_DAEMON)
def fixture_install_transmission_daemon(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mock installation of ``transmission-daemon``.

    :param monkeypatch: Mock patch environment and attributes.
    """
    monkeypatch.setattr("shutil.which", lambda x: x)


@pytest.fixture(name="main")
def fixture_main(monkeypatch: pytest.MonkeyPatch) -> MockMainFixture:
    """Pass patched commandline arguments to package's main function.

    :param monkeypatch: Mock patch environment and attributes.
    :return: Function for using this fixture.
    """

    def _main(*args: str) -> None:
        """Run main with custom args."""
        monkeypatch.setattr(
            "sys.argv", [turba.__name__, *[str(a) for a in args]]
        )
        return turba.main()

    return _main
