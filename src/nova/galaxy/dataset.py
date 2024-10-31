"""
    Datasets
"""
from abc import ABC
from enum import Enum
from bioblend.galaxy.datasets import DatasetClient
from bioblend.galaxy.dataset_collections import DatasetCollectionClient
from typing import Any, Dict, Union
from .data_store import Datastore
from .nova import Nova



class DataState(Enum):
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

    def __init__(self) -> None:
        super().__init__()
        self.path: str = ""
        self.id: Union[str, None] = ""
        self.store: Union[None, Datastore] = None

    def upload(self, store: Datastore) -> None:
        raise NotImplementedError()

    def download(self, local_path: str) -> None:
        raise NotImplementedError()

    def cancel_upload(self) -> None:
        raise NotImplementedError()


class Dataset(AbstractData):

    def __init__(self, path: str):
        self.path = path


    def upload(self, store: Datastore) -> None:
        self.store = store
        self.id = None

    def download(self, local_path: str) -> None:
        if self.store and self.id:
            dataset_client = DatasetClient(self.store.nova.galaxy_instance)
            dataset_client.download_dataset(self.id, file_path=local_path)
            dataset_client.wait_for_dataset(self.id)




class DatasetCollection(AbstractData):

    def __init__(self, path: str):
        self.path = path

    def upload(self, store: Datastore) -> None:
        self.store = store
        # won't be none
        self.id = None

    def download(self, local_path: str) -> None:
        if self.store and self.id:
            dataset_client = DatasetCollectionClient(self.store.nova.galaxy_instance)
            dataset_client.download_dataset_collection(self.id, file_path=local_path)
            dataset_client.wait_for_dataset_collection(self.id)



def upload_datasets(store: Datastore, datasets: Dict[str, AbstractData]) -> Dict[str, str]:
    galaxy_instance = store.nova.galaxy_instance
    dataset_client = DatasetClient(galaxy_instance)
    history_id = galaxy_instance.histories.get_histories(name=store.name)[0]["id"]
    dataset_ids = {}
    for name,dataset in datasets.items():
        dataset_id = galaxy_instance.tools.upload_file(path=dataset.path, history_id=history_id)
        dataset_ids[name] = dataset_id
        dataset.id = dataset_id
        dataset.store = store
    for dataset in dataset_ids.values():
        dataset_client.wait_for_dataset(dataset['outputs'][0]['id'])
    return dataset_ids
