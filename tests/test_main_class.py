"""Test package."""

from nova.galaxy import NOVA


def test_namespace() -> None:
    nova = NOVA()
    nova.namespace = "test"
    assert nova.namespace == "test"
