"""Tests for datasets."""

from nova.galaxy.connection import Connection
from nova.galaxy.dataset import Dataset, DatasetCollection


def test_dataset_upload(nova_instance: Connection) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        input = Dataset("tests/test_files/test_text_file.txt")
        input.upload(store)
        assert input.get_content() is not None


def test_dataset_collection_upload(nova_instance: Connection) -> None:

   galaxy_url = "https://calvera-test.ornl.gov"
   galaxy_key = "1a184ebe45a28b908319308f36d506cb"
   nova = Connection(galaxy_url, galaxy_key)

   files = ["tests/test_files/test_text_file.txt", "tests/test_files/test_text_file.txt"]
   with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        collection = DatasetCollection(files, "test_collection")
        collection.upload(store)
        assert collection.get_content() is not None
