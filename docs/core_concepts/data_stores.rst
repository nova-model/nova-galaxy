.. _data_stores:

Data Stores
-------------------------

A `Datastore` in nova-galaxy represents a Galaxy history. It serves as a container for organizing your data and tool outputs within Galaxy.

.. code-block:: python

    from nova.galaxy import Nova

    galaxy_url = "your_galaxy_url"
    galaxy_key = "your_galaxy_api_key"
    nova = Nova(galaxy_url, galaxy_key)

    with nova.connect() as conn:
        data_store = conn.create_data_store("My Data Store")

You can also choose to persist a data store, preventing the tools in the data store from being automatically stopped when the nova-galaxy connection is closed:

.. code-block:: python

   data_store.persist()
