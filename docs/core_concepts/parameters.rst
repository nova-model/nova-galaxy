.. _parameters:

Parameters
-------------------------

The `Parameters` class is used to define the input parameters for a Galaxy tool.

.. code-block:: python

   from nova.galaxy import Parameters, Dataset

   # Create a dataset from a local file
   my_dataset = Dataset("path/to/my/file.txt")

   # Define tool parameters
   params = Parameters()
   params.add_input("input_file", my_dataset)
   params.add_input("param_name", "param_value")

   # Change an existing input value
   params.change_input_value("param_name", "new_value")

   # Remove an input
   params.remove_input("param_name")