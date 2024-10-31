"""
The NOVA class is responsible for managing interactions with a Galaxy server instance.

It supports operations such as running tools, retrieving job statuses, and fetching job outputs.
The NOVA class abstracts these operations to allow easy integration into other Python applications and scripts.
"""

import os
import zipfile
from io import BytesIO
from typing import Any, Callable, Dict, List, Optional

from bioblend import galaxy
from bioblend.galaxy.tools.inputs import inputs

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
    Class to manage NOVA instance interactions for running and managing reductions.

    Attributes
    ----------
        galaxy_url (Optional[str]): URL of the Galaxy instance.
        galaxy_api_key (Optional[str]): API key for the Galaxy instance.
        namespace (str): Namespace for Galaxy histories.
    """

    def __init__(
        self,
        galaxy_url: Optional[str] = None,
        galaxy_key: Optional[str] = None,
    ) -> None:
        """
        Initializes the NOVA instance with the provided URL and API key.

        Creates a new instance of NOVA, or falls back to environment variables if they are not provided.

        Args:
            galaxy_url (Optional[str]): URL of the Galaxy instance.
            galaxy_key (Optional[str]): API key for the Galaxy instance.
            namespace (str): Namespace for Galaxy histories.
        """
        self.galaxy_url = galaxy_url or os.getenv("GALAXY_URL")
        self.galaxy_api_key = galaxy_key or os.getenv("GALAXY_API_KEY")


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


    def create_data_store(self, name: str) -> Datastore:
        self.galaxy_instance.histories.create_history(name=name)["id"]
        return Datastore(name, self)
