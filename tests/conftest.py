"""Config for testing."""

import os

import pytest
from bioblend.galaxy import GalaxyInstance

from nova.galaxy.connection import Connection

GALAXY_URL = os.environ.get("NOVA_GALAXY_TEST_GALAXY_URL", "https://calvera-test.ornl.gov")
GALAXY_API_KEY = os.environ.get("NOVA_GALAXY_TEST_GALAXY_KEY")


@pytest.fixture
def nova_instance() -> Connection:
    nova = Connection(GALAXY_URL, GALAXY_API_KEY)  # type: ignore
    return nova


@pytest.fixture
def galaxy_instance() -> GalaxyInstance:
    galaxy = GalaxyInstance(url=GALAXY_URL, key=GALAXY_API_KEY)  # type: ignore
    return galaxy
