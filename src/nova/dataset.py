"""
    Datasets
"""
from abc import ABC
from enum import Enum
from bioblend.galaxy.datasets import DatasetClient, DatasetCollectionClient
from .data_store import Datastore





def upload_datasets() -> None:
    pass


class DataState(Enum):
    NONE = 1
    IN_GALAXY = 2
    UPLOADING = 3



class AbstractData(ABC):

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
