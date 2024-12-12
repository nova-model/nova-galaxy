.. _tools:

Tools
--------------

The `Tool` class represents a Galaxy tool. You can run tools, manage their inputs, and retrieve their outputs using nova-galaxy.

.. code-block:: python

   from nova.galaxy import Tool, Parameters, Dataset

   # Get a tool instance
   my_tool = Tool("tool_id")

   # Run the tool
   outputs = my_tool.run(data_store, params)
