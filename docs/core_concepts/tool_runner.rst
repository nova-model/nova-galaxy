.. _tool_runner:

Tool Runner
--------------

The `ToolRunner` is a helper class to run Galaxy tools using Blinker signals. This allows connect to connect
Galaxy with GUI in a decoupled way.

.. code-block:: python

   import blinker
   from nova.galaxy import ToolRunner
   from nova.common.signals import Signal, ToolCommand, get_signal_id


   # create tool runner
   ToolRunner("runner_id", SomeTool(), lambda: "store_name", GALAXY_URL, GALAXY_API_KEY)

   # from somewhere else, e.g. reacting to a button click:
   async def start_tool():
       execution_signal = blinker.signal(get_signal_id("runner_id", Signal.TOOL_COMMAND))
       await execution_signal.send_async("sender_id", command=ToolCommand.START)

The ToolRunner needs a Tool class which it will manage. This class should inherit from the `BasicTool` and define
functions specific to the tool. For example:

.. code-block:: python

    from nova.galaxy import BasicTool
    from nova.galaxy import Connection, Parameters, Tool

    class RemoteCommandTool(BasicTool):
        """Class that prepares RemoteCommandTool tool."""

        def __init__(self) -> None:
            super().__init__()

        def prepare_tool(self) -> Tool:
            tool_params = Parameters()
            tool = Tool(id="neutrons_remote_command")
            return tool, tool_params

        def get_results(self, tool: Tool) -> bytes:
            outputs = tool.get_results()
            data = outputs.get_dataset("output1")
            return data.get_content()
