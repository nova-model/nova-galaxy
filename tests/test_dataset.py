"""Tests for datasets."""

import pytest
from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.datasets import DatasetClient

from nova.galaxy.connection import Connection
from nova.galaxy.dataset import Dataset

REMOTE_FILE_PATH = ""


def test_dataset_upload(nova_instance: Connection) -> None:
    with nova_instance.connect() as connection:
        store = connection.get_data_store(name="nova_galaxy_testing")
        store.mark_for_cleanup()
        input = Dataset("tests/test_files/test_text_file.txt")
        input.upload(store)
        assert input.get_content() is not None


def test_dataset_set_content_upload(nova_instance: Connection) -> None:
    with nova_instance.connect() as connection:
        store = connection.get_data_store(name="nova_galaxy_testing")
        store.mark_for_cleanup()
        input = Dataset()
        # File type is optional
        input.set_content(content="this is some content, that I'm setting", file_type=".txt")
        input.upload(store)
        assert input.get_content() is not None


@pytest.mark.skip
def test_remote_file_ingest(nova_instance: Connection, galaxy_instance: GalaxyInstance) -> None:
    with nova_instance.connect() as connection:
        store = connection.get_data_store(name="nova_galaxy_testing")
        store.mark_for_cleanup()
        data = Dataset(path=REMOTE_FILE_PATH, remote_file=True)
        data.upload(store=store)
        dataset_client = DatasetClient(galaxy_instance)
        dataset_upstream = dataset_client.show_dataset(dataset_id=data.id)
        assert dataset_upstream is not None


def test_dataset_collection_upload(nova_instance: Connection) -> None:
    # TODO: Dataset collection uploading needs to be implemented
    pass
