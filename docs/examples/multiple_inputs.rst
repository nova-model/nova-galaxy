.. _multiple_inputs:

Example 2: Running a Tool with Multiple Inputs
------------------------------------------------

This example shows how to run a tool that takes multiple datasets as input.

.. code-block:: python

   from nova.galaxy import Nova, Dataset, Tool, Parameters, upload_datasets

   galaxy_url = "your_galaxy_url"
   galaxy_key = "your_galaxy_api_key"
   nova = Connection(galaxy_url, galaxy_key)

   with nova.connect() as conn:
       data_store = conn.create_data_store("Multi-Input Example")

       # Create multiple datasets
       dataset1 = Dataset("path/to/file1.txt", name="File 1")
       dataset2 = Dataset("path/to/file2.txt", name="File 2")

       # Upload multiple datasets in parallel
       upload_datasets(data_store, {"input1": dataset1, "input2": dataset2})

       # Define parameters, using the uploaded datasets
       params = Parameters()
       params.add_input("input1", dataset1)
       params.add_input("input2", dataset2)
       params.add_input("some_other_parameter", "some_value")

       # Get and run the tool
       my_tool = Tool("cat1") # Replace with the appropriate tool ID
       outputs = my_tool.run(data_store, params)

       # Process outputs
       # ...
