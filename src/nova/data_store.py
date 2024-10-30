"""
    DataStore
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nova import Nova  # Only imports for type checking

class Datastore:

    def __init__(self, name: str, nova_instance: "Nova"):
        self.name = name
        self.nova = nova_instance
