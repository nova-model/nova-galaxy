"""The NOVA class is responsible for managing interactions with a Galaxy server instance."""

from typing import Optional

from bioblend import galaxy

from .data_store import Datastore


class GalaxyConnectionError(Exception):
    """Exception raised for errors in the connection.

    Attributes
    ----------
        message (str): Explanation of the error.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class Nova:
    """
    Class to manage a Galaxy connection.

    Attributes
    ----------
        galaxy_url (Optional[str]): URL of the Galaxy instance.
        galaxy_api_key (Optional[str]): API key for the Galaxy instance.
    """

    def __init__(
        self,
        galaxy_url: Optional[str] = None,
        galaxy_key: Optional[str] = None,
    ) -> None:
        """
        Initializes the Nova instance with the provided URL and API key.

        Args:
            galaxy_url (Optional[str]): URL of the Galaxy instance.
            galaxy_key (Optional[str]): API key for the Galaxy instance.
        """
        self.galaxy_url = galaxy_url
        self.galaxy_api_key = galaxy_key
        self.galaxy_instance: galaxy.GalaxyInstance

    def connect(self) -> None:
        """
        Connects to the Galaxy instance using the provided URL and API key.

        Raises a ValueError if the URL or API key is not provided.

        Raises
        ------
            ValueError: If the Galaxy URL or API key is not provided.
        """
        if not self.galaxy_url or not self.galaxy_api_key:
            raise ValueError("Galaxy URL and API key must be provided or set in environment variables.")
        if not isinstance(self.galaxy_url, str):
            raise ValueError("Galaxy URL must be a string")
        self.galaxy_instance = galaxy.GalaxyInstance(url=self.galaxy_url, key=self.galaxy_api_key)
        self.galaxy_instance.config.get_version()

    def create_data_store(self, name: str) -> Datastore:
        """Creates a datastore with the given name."""
        histories = self.galaxy_instance.histories.get_histories(name=name)
        if len(histories) > 0:
            return Datastore(name, self, histories[0]["id"])
        history_id = self.galaxy_instance.histories.create_history(name=name)["id"]
        return Datastore(name, self, history_id)

    def remove_data_store(self, name: str) -> None:
        """Permanently deletes the data store with the given name."""
        history = self.galaxy_instance.histories.get_histories(name=name)[0]["id"]
        self.galaxy_instance.histories.delete_history(history_id=history, purge=True)
