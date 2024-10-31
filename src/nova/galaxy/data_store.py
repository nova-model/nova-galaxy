"""DataStore is used to configure Galaxy to group outputs of a tool together."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nova import Nova  # Only imports for type checking


class Datastore:
    """Groups tool outputs together."""

    def __init__(self, name: str, nova_instance: "Nova"):
        self.name = name
        self.nova = nova_instance
