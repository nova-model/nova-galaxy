"""
The NOVA class is responsible for managing interactions with a Galaxy server instance.

It supports operations such as running tools, retrieving job statuses, and fetching job outputs.
The NOVA class abstracts these operations to allow easy integration into other Python applications and scripts.
"""

import os
import zipfile
from io import BytesIO
from typing import Any, Callable, Dict, List, Optional

import bioblend
import requests
from bioblend import galaxy
from bioblend.galaxy.tools.inputs import inputs

from .data_store import Datastore

class DatasetRegistrationError(Exception):
    """
    Exception raised when dataset registration fails.

    Attributes
    ----------
        message (str): Explanation of the error.
        details (Any): Additional details about the error.
    """

    def __init__(self, message: str, details: Any):
        self.message = message
        self.details = details
        super().__init__(self.message, self.details)


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
        namespace: str = "default",
    ) -> None:
        """
        Initializes the NOVA instance with the provided URL and API key.

        Creates a new instance of NOVA, or falls back to environment variables if they are not provided.

        Args:
            galaxy_url (Optional[str]): URL of the Galaxy instance.
            galaxy_key (Optional[str]): API key for the Galaxy instance.
            namespace (str): Namespace for Galaxy histories.
        """
        if not namespace:
            raise ValueError("Namespace cannot be empty.")
        self.galaxy_url = galaxy_url or os.getenv("GALAXY_URL")
        self.galaxy_api_key = galaxy_key or os.getenv("GALAXY_API_KEY")
        self._namespace = namespace

    @property
    def namespace(self) -> str:
        """Get namespace."""
        return self._namespace

    @namespace.setter
    def namespace(self, value: str) -> None:
        """Set namespace."""
        if not value:
            raise ValueError("Namespace cannot be empty.")
        self._namespace = value

    @property
    def history_id(self) -> str:
        """Get or create history ID based on the current namespace."""
        return self._get_history_id(self._namespace)

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


    def get_histories(self, name: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Retrieves a list of histories from the Galaxy server, optionally filtering by name.

        Args:
            name (Optional[str]): Optional pre-specified history name.

        Returns
        -------
            List[Dict[str, str]]: List of histories with their names and IDs.
        """
        histories = self.galaxy_instance.histories.get_histories(name=name)
        return [{"name": history["name"], "id": history["id"]} for history in histories]

    def _get_history_id(self, history_name: str) -> str:
        """
        Retrieves the ID of a history from the Galaxy server based on the provided history name.

        If no history exists with the specified name, a new one is created.

        Args:
            history_name (str): The name of the history.

        Returns
        -------
            str: The history ID.

        Raises
        ------
            bioblend.ConnectionError: If there is an error connecting to the Galaxy server.
        """
        try:
            histories = self.get_histories(name=history_name)
            if histories:
                return histories[0]["id"]

            new_history = self.galaxy_instance.histories.create_history(history_name)
            return new_history["id"]
        except bioblend.ConnectionError as error:
            raise RuntimeError(f"Failed to create history with name {history_name}. Error: {error}") from error

    def _wait_for_ingested_dataset(self, result_dataset_id: str) -> None:
        """
        Waits for the ingested dataset to be ready.

        Args:
            result_dataset_id (str): The ID of the dataset.

        Raises
        ------
            DatasetRegistrationError: If the dataset registration fails.
        """
        dataset_client = galaxy.datasets.DatasetClient(self.galaxy_instance)
        wait_res = dataset_client.wait_for_dataset(result_dataset_id, check=False)
        if wait_res["state"] != "ok":
            details = self.galaxy_instance.histories.show_dataset_provenance(self.namespace, result_dataset_id)
            raise DatasetRegistrationError("Register failed: ", details)

    def ingest_run_numbers(
        self,
        facility: str,
        instrument: str,
        ipts: str,
        runs_to_register: List[int],
        cancel_callback: Optional[Callable[[], bool]] = None,
    ) -> List[str]:
        """
        Ingests datasets based on the provided run list.

        Args:
            facility (str): Base path for the data.
            instrument (str): Instrument name.
            ipts (str): IPTS name.
            runs_to_register (List[int]): List of run numbers to register.
            cancel_callback (Optional[Callable[[], bool]]): Optional callback to cancel operation.

        Returns
        -------
            List[str]: List of dataset IDs.
        """
        n_files = len(runs_to_register)
        tool_inputs = inputs()
        for i in range(n_files):
            fname = f"/{facility}/{instrument}/{ipts}/nexus/" f"{instrument}_{runs_to_register[i]}.nxs.h5"
            tool_inputs = tool_inputs.set_param(f"series_{i}|input", fname)

        meta = None
        if cancel_callback is None or not cancel_callback():
            meta = self.galaxy_instance.tools.run_tool(self.history_id, "neutrons_register", tool_inputs)

        if meta is None:
            return []

        for output in meta["outputs"]:
            if cancel_callback is None or not cancel_callback():
                self._wait_for_ingested_dataset(output["id"])
            else:
                return []

        return [output["id"] for output in meta["outputs"]]

    def upload_file(self, file_path: str, name: Optional[str] = None) -> str:
        """
        Uploads a file to the Galaxy server using the current history.

        Args:
            file_path (str): Path to the file.

        Returns
        -------
            str: The dataset ID of the uploaded file.

        Raises
        ------
            RuntimeError: If the file upload fails.
        """
        try:
            result = self.galaxy_instance.tools.upload_file(file_path, self.history_id, file_name=name)
            return result["outputs"][0]["id"]
        except (IOError, KeyError, bioblend.ConnectionError, ValueError) as error:
            raise RuntimeError(f"Failed to upload file: {error}") from error

    def download_result(self, dataset_id: str, save_path: str) -> str:
        """
        Downloads a dataset from Galaxy.

        Args:
            dataset_id (str): The ID of the dataset to download.
            save_path (str): The local path to save the downloaded file.

        Raises
        ------
            RuntimeError: If the dataset cannot be downloaded.
        """
        if not os.path.exists(save_path):
            os.makedirs(save_path)  # Create the directory if it doesn't exist

        base_url = f"{self.galaxy_url}/api/dataset_collections/"
        api_key_param = f"key={self.galaxy_api_key}"
        url = f"{base_url}{dataset_id}/download?{api_key_param}"

        headers = {"X-API-Key": self.galaxy_api_key}

        try:
            # Fetching the zip file from the server
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()

            # Open the zip file
            with zipfile.ZipFile(BytesIO(response.content)) as downloaded_zip:
                # Extract each file into the directory
                downloaded_zip.extractall(save_path)
            print(f"Files extracted to {save_path}")
            return save_path
        except requests.exceptions.RequestException as error:
            raise RuntimeError(f"Failed to download dataset {dataset_id}. Error: {error}") from error
        except zipfile.BadZipFile as zip_error:
            raise RuntimeError(f"Failed to extract zip file. Error: {zip_error}") from zip_error

def main():
    print("hello")