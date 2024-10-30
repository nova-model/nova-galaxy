"""
    DataStore
"""

from .nova import Nova


class Datastore:

    def __init__(self, name: str, nova_instance: Nova):
        self.name = name
        self.nova = nova_instance
