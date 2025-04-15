"""Tests for tools."""

import time

from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.datasets import DatasetClient

from nova.galaxy.connection import Connection
from nova.galaxy.dataset import Dataset, DatasetCollection, upload_datasets
from nova.galaxy.parameters import Parameters
from nova.galaxy.workflow import Workflow
from nova.galaxy.util import WorkState

TEST_TOOL_ID = "c6a6723b4597bbc7"
TEST_INT_TOOL_ID = "interactive_tool_generic_output"


def test_run_workflow(nova_instance: Connection) -> None:
    

    galaxy_url = "https://calvera-test.ornl.gov"
    galaxy_key = "1a184ebe45a28b908319308f36d506cb"
    nova = Connection(galaxy_url, galaxy_key)

    files = ["tests/test_files/test_text_file.txt", "tests/test_files/test_text_file.txt"]

    with nova.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        test_workflow = Workflow(TEST_TOOL_ID)
        
        # Create multiple datasets
        dataset1 = Dataset("data/prepare_peaks_manifest.csv", name="Manifest File")
        dataset2 = Dataset("data/goniometer.csv", name="Goniometer File")

        # Upload multiple datasets in parallel
        upload_datasets(store, {"Manifest File": dataset1, "Goniometer File": dataset2})
        
        collection = DatasetCollection(
                    ["data/image_bank_id_1.png",
                    "data/image_bank_id_2.png",
                    "data/image_bank_id_3.png",
                    "data/image_bank_id_4.png",
                    "data/image_bank_id_5.png",
                    "data/image_bank_id_6.png",
                    "data/image_bank_id_7.png",
                    "data/image_bank_id_8.png",
                    "data/image_bank_id_9.png",
                    "data/image_bank_id_10.png",
                    "data/image_bank_id_11.png",
                    "data/image_bank_id_12.png",
                    "data/image_bank_id_13.png",
                    "data/image_bank_id_14.png",
                    "data/image_bank_id_15.png",
                    "data/image_bank_id_16.png",
                    "data/image_bank_id_17.png",
                    "data/image_bank_id_18.png",
                    "data/image_bank_id_19.png",
                    "data/image_bank_id_20.png",
                    "data/image_bank_id_21.png",
                    "data/image_bank_id_22.png",
                    "data/image_bank_id_23.png",
                    "data/image_bank_id_24.png",
                    "data/image_bank_id_25.png",
                    "data/image_bank_id_26.png",
                    "data/image_bank_id_27.png",
                    "data/image_bank_id_28.png",
                    "data/image_bank_id_29.png",
                    "data/image_bank_id_30.png",
                    "data/image_bank_id_31.png",
                    "data/image_bank_id_32.png",
                    "data/image_bank_id_33.png",
                    "data/image_bank_id_34.png",
                    "data/image_bank_id_35.png",
                    "data/image_bank_id_36.png",
                    "data/image_bank_id_37.png",
                    "data/image_bank_id_38.png",
                    "data/image_bank_id_39.png",
                    "data/image_bank_id_40.png",
                    "data/image_bank_id_41.png"
                    ], store)
        
        params = Parameters()
        params.add_input("Min Wavelength", 2)
        params.add_input("Max Wavelength", 4)
        params.add_input("a", 18.39)
        params.add_input("b", 56.55)
        params.add_input("c", 6.54)
        params.add_input("Alpha", 90)
        params.add_input("Beta", 90)
        params.add_input("Gamma", 90)
        params.add_input("Sample Centering", "Face Centered")
        params.add_input("Manifest File", dataset1)
        params.add_input("Goniometer File", dataset2)
        params.add_input("Image files", collection)
        
        outputs = test_workflow.run(data_store=store, params=params)
        assert outputs is not None
        data = outputs.get_dataset("output1")
        assert "hostname:" in data.get_content()

# def test_status(nova_instance: Connection) -> None:
#     with nova_instance.connect() as connection:
#         store = connection.create_data_store(name="nova_galaxy_testing")
#         test_tool = Tool(TEST_INT_TOOL_ID)
#         params = Parameters()
#         state = test_tool.get_status()
#         assert state == WorkState.NOT_STARTED
#         test_tool.run_interactive(data_store=store, params=params, check_url=False)
#         state = test_tool.get_status()
#         assert state == WorkState.RUNNING
#         test_tool.stop()
#         state = test_tool.get_status()
#         assert state == WorkState.FINISHED
#
#
# def test_cancel_tool(nova_instance: Connection) -> None:
#     with nova_instance.connect() as connection:
#         store = connection.create_data_store(name="nova_galaxy_testing")
#         test_tool = Tool(TEST_INT_TOOL_ID)
#         params = Parameters()
#         test_tool.run_interactive(data_store=store, params=params, check_url=False)
#         test_tool.cancel()
#         state = test_tool.get_status()
#         assert state == WorkState.ERROR
#
#
# def test_get_tool_stdout(nova_instance: Connection) -> None:
#     with nova_instance.connect() as connection:
#         store = connection.create_data_store(name="nova_galaxy_testing")
#         test_tool = Tool(TEST_INT_TOOL_ID)
#         params = Parameters()
#         test_tool.run_interactive(data_store=store, params=params, check_url=False)
#         state = test_tool.get_status()
#         assert state == WorkState.RUNNING
#         time.sleep(10)  # Tool takes a moment to produce stdout
#         stdout = test_tool.get_stdout()
#         assert stdout is not None
#         test_tool.cancel()
