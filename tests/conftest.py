import os
import shutil
import pytest

from manven import settings
# Set a temporary directory to use for the tests
path_to_here = os.path.dirname(os.path.abspath(__file__))
settings.ENVS_PATH = os.path.join(path_to_here, ".tmp")


@pytest.fixture()
def teardown():
    yield
    if os.path.exists(settings.ENVS_PATH):
        shutil.rmtree(settings.ENVS_PATH)
