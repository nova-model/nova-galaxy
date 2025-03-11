.. _interactive_tools:

Interactive Tools
-----------------

nova-galaxy allows running Galaxy tools in interactive mode, which is especially useful when tools generate URLs that need to be accessed during runtime.

.. code-block:: python

    from nova.galaxy import Tool, Parameters

    # Define tool parameters
    params = Parameters()

    # Get a tool instance
    my_tool = Tool("tool_id") # Replace with your tool id from Galaxy

    # Run the tool in interactive mode
    url = my_tool.run_interactive(data_store, params)
    print(f"Interactive tool URL: {url}")

By default, interactive tools are stopped automatically once the Nova connection is closed. To override this behavior, use the DataStore persist method. This will cause the tool to run into perpetuity and will need to be stopped manually using the Tool stop_all_tools_in_store method.
