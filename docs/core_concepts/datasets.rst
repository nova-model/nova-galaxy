.. _datasets:

Datasets and Dataset Collections
--------------------------------

nova-galaxy provides abstractions for handling individual files (`Dataset`) and collections of files (`DatasetCollection`) within Galaxy.

.. code-block:: python

   from nova.galaxy import Dataset, DatasetCollection

   # Create a Dataset from a local file
   my_dataset = Dataset("path/to/my/file.txt")

   # Create a DatasetCollection (implementation for upload pending)
   my_collection = DatasetCollection("path/to/my/collection")
