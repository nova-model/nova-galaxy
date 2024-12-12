"""Tests for data stores."""

from bioblend.galaxy import GalaxyInstance

from nova.galaxy.nova import Nova


def test_no_persist_store(nova_instance: Nova, galaxy_instance: GalaxyInstance) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        history = galaxy_instance.histories.get_histories(name=store.name)
        assert len(history) > 0
    history = galaxy_instance.histories.get_histories(name=store.history_id, deleted=False)
    assert len(history) < 1


def test_persist_store(nova_instance: Nova, galaxy_instance: GalaxyInstance) -> None:
    with nova_instance.connect() as connection:
        store = connection.create_data_store(name="nova_galaxy_testing")
        store.persist()
        history = galaxy_instance.histories.get_histories(name=store.name)
        assert len(history) > 0
    history = galaxy_instance.histories.get_histories(name=store.name, deleted=False)
    assert len(history) > 0
    # TODO: Can maybe do global cleanup
    galaxy_instance.histories.delete_history(history_id=history[0]["id"], purge=True)
