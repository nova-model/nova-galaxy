"""Test package."""

from ndip_galaxy import MainClass


def test_version() -> None:
    ndip_galaxy = MainClass()
    assert ndip_galaxy.name("test") == "test"
