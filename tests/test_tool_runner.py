"""Tests for tools."""

import asyncio
import os
from typing import Any, Dict

import blinker
import pytest

from nova.common.job import WorkState
from nova.common.signals import Signal, ToolCommand, get_signal_id
from nova.galaxy import Connection, Parameters, Tool
from nova.galaxy.interfaces import BasicTool
from nova.galaxy.tool_runner import ToolRunner

GALAXY_URL = os.environ.get("NOVA_GALAXY_TEST_GALAXY_URL", "https://calvera-test.ornl.gov")
GALAXY_API_KEY = os.environ.get("NOVA_GALAXY_TEST_GALAXY_KEY")


class RemoteCommandTool(BasicTool):
    """Class that prepares RemoteCommandTool tool."""

    def __init__(self) -> None:
        super().__init__()

    def prepare_data(self) -> None:
        pass

    def prepare_tool(self) -> Tool:
        tool_params = Parameters()
        tool = Tool(id="neutrons_remote_command")
        return tool, tool_params

    def get_results(self, tool: Tool) -> bytes:
        outputs = tool.get_results()
        data = outputs.get_dataset("output1")
        return data.get_content()

    def validate_for_run(self) -> None:
        pass


# this is not how it is usually works since different parts would be in different components. But here we put everything
# in one place to test
@pytest.mark.asyncio
async def test_tool_runner(nova_instance: Connection) -> None:
    id = "test"
    ToolRunner(id, RemoteCommandTool(), lambda: "nova_galaxy_testing", GALAXY_URL, GALAXY_API_KEY)
    execution_signal = blinker.signal(get_signal_id(id, Signal.TOOL_COMMAND))
    progress_signal = blinker.signal(get_signal_id(id, Signal.PROGRESS))
    await execution_signal.send_async(id, command=ToolCommand.START)

    # setup state change callback and update results
    results: Dict[str, Any] = {"res": None}

    async def update_state(_sender: Any, state: WorkState, details: str) -> None:
        if state == WorkState.FINISHED:
            responses = await execution_signal.send_async("test", command=ToolCommand.GET_RESULTS)
            results["res"] = responses[0][1]["results"]
        elif state == WorkState.ERROR:
            results["res"] = b"error"

    progress_signal.connect(update_state, weak=False)

    # waiting for results to be updated
    for _ in range(60):
        if results["res"] is not None:
            break
        await asyncio.sleep(1)

    # to delete Galaxy history
    with nova_instance.connect() as connection:
        store = connection.get_data_store(name="nova_galaxy_testing")
        store.mark_for_cleanup()

    assert results["res"] is not None
    assert "hostname:" in results["res"].decode("utf-8")
