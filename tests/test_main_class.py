"""Test package."""

from ndip_galaxy import NDIP

def test_namespace() -> None:
    ndip_galaxy = NDIP()
    ndip_galaxy.namespace = "test"
    assert ndip_galaxy.namespace == "test"