from nova.galaxy.parameters import Parameters
from nova.galaxy.tool import Tool, WorkState

TEST_INT_TOOL_ID = "interactive_tool_generic_output"


def test_status(nova_instance, galaxy_instance):
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        state = test_tool.get_status()
        assert state == WorkState.NOT_STARTED
        link = test_tool.run_interactive(data_store=store, params=params, check_url=False)
        state = test_tool.get_status()
        test_tool.get_results()
        assert state == WorkState.RUNNING
        test_tool.stop()
        state = test_tool.get_status()
        assert state == WorkState.FINISHED


def test_cancel_tool(nova_instance, galaxy_instance):
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        link = test_tool.run_interactive(data_store=store, params=params, check_url=False)
        test_tool.cancel()
        state = test_tool.get_status()
        assert state == WorkState.ERROR


def test_get_tool_stdout(nova_instance):
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        link = test_tool.run_interactive(data_store=store, params=params, check_url=False)
        state = test_tool.get_status()
        assert state == WorkState.RUNNING
        stdout = test_tool.get_stdout()
        assert stdout is not None  # TODO maybe check specific stdout here
