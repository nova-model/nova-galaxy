"""DataStore is used to configure Galaxy to group outputs of a tool together."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nova import NovaConnection  # Only imports for type checking


class Datastore:
    """Groups tool outputs together.

    The constructor is not intended for external use. Use nova.galaxy.Nova.create_data_store() instead.
    """

    def __init__(self, name: str, nova_connection: "NovaConnection", history_id: str) -> None:
        self.name = name
        self.nova_connection = nova_connection
        self.history_id = history_id
        self.persist_store = False

    def persist(self) -> None:
        self.persist_store = True
