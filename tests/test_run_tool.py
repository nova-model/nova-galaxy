"""Tests for tools."""

import time

from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.datasets import DatasetClient

from nova.galaxy.connection import Connection
from nova.galaxy.dataset import Dataset
from nova.galaxy.parameters import Parameters
from nova.galaxy.tool import Tool
from nova.galaxy.util import WorkState

TEST_TOOL_ID = "neutrons_remote_command"
TEST_INT_TOOL_ID = "interactive_tool_generic_output"


def test_run_tool(nova_instance: Connection) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        store.mark_for_cleanup()
        test_tool = Tool(TEST_TOOL_ID)
        outputs = test_tool.run(data_store=store, params=Parameters())
        assert outputs is not None
        data = outputs.get_dataset("output1")
        assert "hostname:" in data.get_content()


def test_run_tool_interactive(nova_instance: Connection, galaxy_instance: GalaxyInstance) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        store.mark_for_cleanup()
        notebook = Dataset(path="tests/test_files/test_jupyter_notebook.ipynb")
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        params.add_input("mode|mode_select", "previous")
        params.add_input("ipynb", notebook)
        params.add_input("run_it", True)
        link = test_tool.run_interactive(data_store=store, params=params, check_url=False)
        assert link is not None
        assert test_tool.get_url() is not None
        entry_points = galaxy_instance.make_get_request(
            f"{store.nova_connection.galaxy_url}/api/entry_points?running=true"
        )
        for ep in entry_points.json():
            if ep.get("target", None):
                if link == f"{store.nova_connection.galaxy_url}{ep['target']}":
                    galaxy_instance.jobs.wait_for_job(job_id=ep["job_id"])
                    outputs = galaxy_instance.jobs.get_outputs(ep["job_id"])
                    test_output = None
                    for out in outputs:
                        if out.get("name", None) == "output_single":
                            test_output = out["dataset"]["id"]
                    assert test_output is not None
                    dataset_client = DatasetClient(store.nova_connection.galaxy_instance)
                    test_text = dataset_client.download_dataset(
                        test_output, use_default_filename=False, file_path=None
                    ).decode("utf-8")
                    assert test_text == "this is a test"
                    return
        raise Exception("Did not find interactive tool while testing.")


def test_status(nova_instance: Connection) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        store.mark_for_cleanup()
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        state = test_tool.get_status()
        assert state == WorkState.NOT_STARTED
        test_tool.run_interactive(data_store=store, params=params, check_url=False)
        state = test_tool.get_status()
        assert state == WorkState.RUNNING
        test_tool.stop()
        state = test_tool.get_status()
        assert state == WorkState.FINISHED


def test_cancel_tool(nova_instance: Connection) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        store.mark_for_cleanup()
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        test_tool.run_interactive(data_store=store, params=params, check_url=False)
        test_tool.cancel()
        state = test_tool.get_status()
        assert state == WorkState.ERROR


def test_get_tool_stdout(nova_instance: Connection) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        store.mark_for_cleanup()
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        test_tool.run_interactive(data_store=store, params=params, check_url=False)
        state = test_tool.get_status()
        assert state == WorkState.RUNNING
        time.sleep(10)  # Tool takes a moment to produce stdout
        stdout = test_tool.get_stdout()
        assert stdout is not None
        test_tool.cancel()
