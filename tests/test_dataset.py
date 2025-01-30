"""Tests for datasets."""

from nova.galaxy.connection import Connection
from nova.galaxy.dataset import Dataset


def test_dataset_upload(nova_instance: Connection) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        input = Dataset("tests/test_files/test_text_file.txt")
        input.upload(store)
        assert input.get_content() is not None


def test_dataset_collection_upload(nova_instance: Connection) -> None:
    # TODO: Dataset collection uploading needs to be implemented
    pass
