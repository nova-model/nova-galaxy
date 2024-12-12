.. _basic_usage:

Example 1: Uploading a Dataset and Running a Tool
--------------------------------------------------

This example demonstrates how to upload a dataset to Galaxy and run a tool using nova-galaxy.

.. code-block:: python

   from nova.galaxy import Nova, Dataset, Tool, Parameters

   galaxy_url = "your_galaxy_url"
   galaxy_key = "your_galaxy_api_key"
   nova = Nova(galaxy_url, galaxy_key)

   with nova.connect() as conn:
       # Create a data store
       data_store = conn.create_data_store("Example Data Store")

       # Create a dataset from a local file
       my_dataset = Dataset("path/to/your/file.txt", name="My Dataset")

       # Upload the dataset to Galaxy
       my_dataset.upload(data_store)

       # Define tool parameters
       params = Parameters()
       params.add_input("input", my_dataset)
       params.add_input("some_parameter", 10)

       # Get the tool
       my_tool = Tool("add_value") # Replace with the actual tool ID

       # Run the tool
       outputs = my_tool.run(data_store, params)

       # Get an output dataset
       output_dataset = outputs.get_dataset("out_file1")

       # Download the output dataset
       output_dataset.download("path/to/output/directory")

       # Get the content of the output dataset
       content = output_dataset.get_content()
       print(content)