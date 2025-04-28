"""Contains Data Abstractions.

AbstractData objects are used to encapsulate data for use in Galaxy tools,
as well as output data from Galaxy tools.
"""

from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Union

from bioblend.galaxy.dataset_collections import DatasetCollectionClient
from bioblend.galaxy.datasets import DatasetClient

if TYPE_CHECKING:
    from .data_store import Datastore


class DataState(Enum):
    """The state of a dataset in Galaxy."""

    NONE = 1
    IN_GALAXY = 2
    UPLOADING = 3


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


class AbstractData(ABC):
    """Encapsulates data for use in Galaxy toools."""

    def __init__(self) -> None:
        super().__init__()
        self.path: str = ""
        self.id: Union[str, None] = ""
        self.name: str = ""
        self.store: Union[None, "Datastore"] = None

    @abstractmethod
    def upload(self, store: "Datastore") -> None:
        raise NotImplementedError()

    @abstractmethod
    def download(self, local_path: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def get_content(self) -> Any:
        raise NotImplementedError()

    def cancel_upload(self) -> None:
        raise NotImplementedError()


class Dataset(AbstractData):
    """Singular file that can be uploaded and used in a Galaxy tool.

    If needing to change the path of the Dataset, it is recommended to create a new Dataset instead.
    """

    def __init__(self, path: str = "", name: Optional[str] = None):
        self.path = path
        self.name = name or Path(path).name
        self.id: str = ""
        self.store: Optional["Datastore"] = None
        self.file_type: str = Path(path).suffix
        self._content: Any = None

    def upload(self, store: "Datastore", name: Optional[str] = None) -> None:
        """Uploads this dataset to the data store given.

        This method will automatically set the id, and store class variables for future use.

        Parameters
        ----------
        store: Datastore
            The data store to upload this dataset to.
        name: Optional[str]
            The name that will be used for the dataset upstream. Defaults to the local name.
        """
        galaxy_instance = store.nova_connection.galaxy_instance
        dataset_client = DatasetClient(galaxy_instance)
        history_id = galaxy_instance.histories.get_histories(name=store.name)[0]["id"]
        if name:
            file_name = name
        else:
            file_name = self.name
        if self._content:
            dataset_info = galaxy_instance.tools.paste_content(
                content=self._content, history_id=history_id, file_name=file_name
            )
        else:
            dataset_info = galaxy_instance.tools.upload_file(path=self.path, history_id=history_id, file_name=file_name)
        self.id = dataset_info["outputs"][0]["id"]
        self.store = store
        dataset_client.wait_for_dataset(self.id)

    def download(self, local_path: str) -> AbstractData:
        """Downloads this dataset to the local path given."""
        if self.store and self.id:
            dataset_client = DatasetClient(self.store.nova_connection.galaxy_instance)
            dataset_client.download_dataset(self.id, use_default_filename=False, file_path=local_path)
            return self
        else:
            raise Exception("Dataset is not present in Galaxy.")

    def set_content(self, content: Any, file_type: str = "") -> None:
        """Directly set the content of this dataset.

        Use this method if instead of having a dataset load from a file, you want to directly pass in content.
        Note, the content must be able to be serialized as a string in order to facilitate the uploading process.
        """
        try:
            str(content)
            self._content = content
            self.file_type = file_type
        except Exception as e:
            raise Exception("Dataset content must be able to be serialized as a string.") from e

    def get_content(self) -> Any:
        """Get the content of this dataset.

        If the content is not already present in memory, this method will download and/or load the file content into
        memory. If not careful, this can cause performance issues with large datasets. For larger files, consider
        using the download() method and writing the file to a local path.
        """
        if self._content:
            return self._content
        try:
            if self.store and self.id:
                dataset_client = DatasetClient(self.store.nova_connection.galaxy_instance)
                self._content = dataset_client.download_dataset(self.id, use_default_filename=False, file_path=None)
            else:
                with open(self.path, "r") as file:
                    self._content = file.read()
        except Exception as e:
            raise Exception(f"Dataset is not present in Galaxy or locally. Error Details: {e}") from e
        return self._content


class DatasetCollection(AbstractData):
    """A group of files that can be uploaded as a collection and collectively be used in a Galaxy tool."""

    def __init__(self, path: str, name: Optional[str] = None):
        self.path = path
        self.name = name or Path(path).name
        self.id: str
        self.store: "Datastore"

    def upload(self, store: "Datastore") -> None:
        """Will need to handle this differently than single datasets."""
        raise NotImplementedError

    def download(self, local_path: str) -> AbstractData:
        """Downloads this dataset collection to the local path given."""
        if self.store and self.id:
            dataset_client = DatasetCollectionClient(self.store.nova_connection.galaxy_instance)
            dataset_client.download_dataset_collection(self.id, file_path=local_path)
            return self
        else:
            raise Exception("Dataset collection is not present in Galaxy.")

    def get_content(self) -> Any:
        """Get a list of the content of this Collection along with info on each element."""
        if self.store and self.id:
            dataset_client = DatasetCollectionClient(self.store.nova_connection.galaxy_instance)
            info = dataset_client.show_dataset_collection(self.id)
            return info["elements"]
        else:
            raise Exception("Dataset collection is not present in Galaxy.")
