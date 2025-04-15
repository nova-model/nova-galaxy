"""Contains Data Abstractions.

AbstractData objects are used to encapsulate data for use in Galaxy tools,
as well as output data from Galaxy tools.
"""

from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from bioblend.galaxy.dataset_collections import DatasetCollectionClient
from bioblend.galaxy.datasets import DatasetClient

if TYPE_CHECKING:
    from .data_store import Datastore

from .parameters import Parameters
from .tool import Tool


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
    """Singular file that can be uploaded and used in a Galaxy tool."""

    def __init__(self, path: str, name: Optional[str] = None):
        self.path = path
        self.name = name or Path(path).name
        self.id: str
        self.store: "Datastore"

    def upload(self, store: "Datastore") -> None:
        galaxy_instance = store.nova_connection.galaxy_instance
        dataset_client = DatasetClient(galaxy_instance)
        history_id = galaxy_instance.histories.get_histories(name=store.name)[0]["id"]
        dataset_id = galaxy_instance.tools.upload_file(path=self.path, history_id=history_id)
        self.id = dataset_id["outputs"][0]["id"]
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

    def get_content(self) -> Any:
        if self.store and self.id:
            dataset_client = DatasetClient(self.store.nova_connection.galaxy_instance)
            return dataset_client.download_dataset(self.id, use_default_filename=False, file_path=None).decode("utf-8")
        else:
            raise Exception("Dataset is not present in Galaxy.")


class DatasetCollection(AbstractData):
    """A group of files that can be uploaded as a collection and collectively be used in a Galaxy tool."""

    def __init__(self, paths: List[str], name: str = ""):
        self.paths = paths
        self.name = name
        self.id: str
        self.store: "Datastore"

    def upload(self, store: "Datastore") -> None:
        """ Upload several files as a collection.

        Parameters
        ----------
        store: "Datastore"
            The Datastore to upload the collection under
        """

        self.store = store

        # Dictionary from file names to Datasets, needed when doing parallel upload
        input_dictionary = {}

        # Parameters for the Build List tool
        params = Parameters()

        # Create a Dataset for each requested path and add it to the dictionary and Parameters
        for i in range(len(self.paths)):
            new_dataset = Dataset(self.paths[i])
            input_dictionary["Input Dataset" + str(i)] = new_dataset
            params.add_input("Input Dataset" + str(i), new_dataset)

        # Parallel upload of all the Datasets
        upload_datasets(store, input_dictionary)

        # Run the Build List tool on all the uploaded datasets, turning them into a DatasetCollection
        build_list_tool = Tool("__BUILD_LIST__")
        outputs = build_list_tool.run(data_store=store, params=Parameters())

        # Return the new DatasetCollection produced by the tool
        print(outputs.data)
        new_collection = outputs.get_dataset("(as list)")
        
        self.id = new_collection.id

    def download(self, local_path: str) -> AbstractData:
        """Downloads this dataset collection to the local path given."""
        if self.store and self.id:
            dataset_client = DatasetCollectionClient(self.store.nova_connection.galaxy_instance)
            dataset_client.download_dataset_collection(self.id, file_path=local_path)
            return self
        else:
            raise Exception("Dataset collection is not present in Galaxy.")

    def get_content(self) -> Any:
        if self.store and self.id:
            dataset_client = DatasetCollectionClient(self.store.nova_connection.galaxy_instance)
            info = dataset_client.show_dataset_collection(self.id)
            self.info = info
            return info
        else:
            raise Exception("Dataset collection is not present in Galaxy.")


def upload_datasets(store: "Datastore", datasets: Dict[str, AbstractData]) -> Dict[str, str]:
    """Helper method to upload multiple datasets or collections in parallel."""
    galaxy_instance = store.nova_connection.galaxy_instance
    dataset_client = DatasetClient(galaxy_instance)
    history_id = galaxy_instance.histories.get_histories(name=store.name)[0]["id"]
    dataset_ids = {}
    for name, dataset in datasets.items():
        dataset_id = galaxy_instance.tools.upload_file(path=dataset.path, history_id=history_id)
        dataset_ids[name] = dataset_id["outputs"][0]["id"]
        dataset.id = dataset_id["outputs"][0]["id"]
        dataset.store = store
    for dataset_output in dataset_ids.values():
        dataset_client.wait_for_dataset(dataset_output)
    return dataset_ids
