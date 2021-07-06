import os
import shutil
import pytest

from manven import settings
# Set a temporary directory to use for the tests
path_to_here = os.path.dirname(os.path.abspath(__file__))
tmp_envs_path = os.path.join(path_to_here, ".tmp")
settings.ENVS_PATH = tmp_envs_path


@pytest.fixture()
def teardown():
    yield
    assert settings.ENVS_PATH == tmp_envs_path  # make sure this hasn't changed
    if os.path.exists(settings.ENVS_PATH):
        shutil.rmtree(settings.ENVS_PATH)
