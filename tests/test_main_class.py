"""Test package."""

from nova import Nova


def test_namespace() -> None:
    nova = Nova()
    nova.namespace = "test"
    assert nova.namespace == "test"
