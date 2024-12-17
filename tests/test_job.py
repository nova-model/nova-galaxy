from nova.galaxy.tool import Tool, WorkState
from nova.galaxy.parameters import Parameters
TEST_INT_TOOL_ID = "interactive_tool_generic_output"

def test_status(nova_instance, galaxy_instance):
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        state = test_tool.status()
        assert state == WorkState.NOT_STARTED
        link = test_tool.run_interactive(data_store=store, params=params, check_url=False)
        state = test_tool.status()
        # state = connection.get_status(test_tool)
        assert state == WorkState.RUNNING
        # TODO: Implement job canceling/stopping, then replace this with that stuff
        test_tool.stop()
        # galaxy_instance.make_get_request(f"{store.nova_connection.galaxy_url}/api/jobs/{test_tool.job_id}/finish")
        # galaxy_instance.wait_for_job(test_tool.job_id)
        state = connection.get_status(test_tool)
        assert state == WorkState.FINISHED


def test_cancel_tool(nova_instance, galaxy_instance):
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        link = test_tool.run_interactive(data_store=store, params=params, check_url=False)
        # TODO: Implement job canceling/stopping, then replace this with that stuff
        test_tool.cancel()
        # state = connection.get_status(test_tool)
        state = test_tool.status()
        assert state == WorkState.ERROR


def test_get_tool_stdout(nova_instance):
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        test_tool = Tool(TEST_INT_TOOL_ID)
        params = Parameters()
        link = test_tool.run_interactive(data_store=store, params=params, check_url=False)
        # TODO: Implement job canceling/stopping, then replace this with that stuff
        state = test_tool.status()
        # state = connection.get_status(test_tool)
        assert state == WorkState.RUNNING
        stdout = test_tool.get_stdout()
        assert stdout is not None # TODO maybe check specific stdout here

