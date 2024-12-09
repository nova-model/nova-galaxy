"""Tests for tools."""

from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.datasets import DatasetClient

from nova.galaxy.dataset import Dataset
from nova.galaxy.nova import Nova
from nova.galaxy.parameters import Parameters
from nova.galaxy.tool import Tool

TEST_TOOL_ID = "neutrons_remote_command"
TEST_INT_TOOL_ID = "interactive_tool_generic_output"


def test_run_tool(nova_instance: Nova) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        test_tool = Tool(TEST_TOOL_ID)
        outputs = test_tool.run(data_store=store, params=Parameters())
        assert outputs is not None
        data = outputs.get_dataset("output1")
        assert "hostname:" in data.get_content()


def test_run_tool_interactive(nova_instance: Nova, galaxy_instance: GalaxyInstance) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        notebook = Dataset(path="tests/test_files/test_jupyter_notebook.ipynb")
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        params.add_input("mode|mode_select", "previous")
        params.add_input("ipynb", notebook)
        params.add_input("run_it", True)
        link = test_tool.run_interactive(data_store=store, params=params, check_url=False)
        assert link is not None
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
