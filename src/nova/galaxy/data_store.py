"""DataStore is used to configure Galaxy to group outputs of a tool together."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nova import Nova  # Only imports for type checking


class Datastore:
    """Groups tool outputs together.

    The constructor is not intended for external use. Use nova.galaxy.Nova.create_data_store() instead.
    """

    def __init__(self, name: str, nova_instance: "Nova", history_id: str):
        self.name = name
        self.nova = nova_instance
        self.history_id = history_id
