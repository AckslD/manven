import os
import pytest

from manven.commands import create_environment, activate_environment, list_environments,\
    remove_environment, deactivate_environment, reset_to_execute,\
    activate_temp_environment, prune_temp_environments,\
    TO_EXECUTE_FILE, _get_activate_script_name
from manven.settings import ENVS_PATH

########################################################################
# NOTE: in conftest.py we set a different path to be used such that we #
# don't mess anything up for the user when testing.                    #
########################################################################


@pytest.mark.parametrize("environment_name", [
    "test",
    "test",
    "hello",
])
def test_create_environment(environment_name, teardown):
    create_environment(environment_name, default_pkgs=[])
    assert os.path.exists(os.path.join(ENVS_PATH, environment_name))


def test_create_replace_environment(teardown):
    environment_name = "test"
    create_environment(environment_name, default_pkgs=[])
    folder_path = os.path.join(ENVS_PATH, environment_name, "tmp_folder")
    os.mkdir(folder_path)
    assert os.path.exists(folder_path)
    # Check that replace=False keeps the folder we made
    create_environment(environment_name, replace=False, default_pkgs=[])
    assert os.path.exists(folder_path)
    # Check that replace=True removes the folder we made
    create_environment(environment_name, replace=True, default_pkgs=[])
    assert not os.path.exists(folder_path)


@pytest.mark.parametrize("environment_name", [
    "test",
    "test",
    "hello",
])
def test_activate_environment(environment_name, teardown):
    create_environment(environment_name, default_pkgs=[])
    activate_environment(environment_name)

    # Read what's in the file to be executed
    with open(TO_EXECUTE_FILE, 'r') as f:
        lines = f.readlines()

    # Check that the content of the file is correct
    assert len(lines) == 1
    line = lines[0]
    activate_script_name = _get_activate_script_name()
    activate_script_path = os.path.join(ENVS_PATH, environment_name, "bin", activate_script_name)
    assert line == f"source {activate_script_path}"


@pytest.mark.parametrize("environment_names, num_temp_envs", [
    (["test"], 0),
    (["test", "hello"], 0),
    (["test", "hello"], 2),
])
def test_list_environments(environment_names, num_temp_envs, teardown):
    """
    Also tests activate_temp_environment and prune_temp_environments
    """
    for environment_name in environment_names:
        create_environment(environment_name, default_pkgs=[])
    for _ in range(num_temp_envs):
        activate_temp_environment(default_pkgs=[])

    environments = list_environments()
    assert sorted(environments) == sorted(environment_names)
    environments = list_environments(include_temporary=True)
    assert sorted(environments) == sorted(environment_names + [f".temp/temp_venv_{i}" for i in range(num_temp_envs)])

    # Prune the temp environments
    prune_temp_environments()
    environments = list_environments(include_temporary=True)
    assert sorted(environments) == sorted(environment_names)


@pytest.mark.parametrize("environment_names, to_remove", [
    (["test"], []),
    (["test"], ["test"]),
    (["test", "hello"], ["other"]),
])
def test_remove_environments(environment_names, to_remove, teardown):
    for environment_name in environment_names:
        create_environment(environment_name, default_pkgs=[])
    for environment_name in to_remove:
        remove_environment(environment_name)

    environments_left = os.listdir(ENVS_PATH)
    environments_left_expected = set(environment_names) - set(to_remove)

    assert sorted(environments_left) == sorted(environments_left_expected)


def test_deactivate():
    deactivate_environment()

    # Read what's in the file to be executed
    with open(TO_EXECUTE_FILE, 'r') as f:
        lines = f.readlines()

    # Check that the content of the file is correct
    assert len(lines) == 1
    line = lines[0]
    assert line == "deactivate"


def test_reset_to_execute():
    os.remove(TO_EXECUTE_FILE)
    reset_to_execute()
    assert os.path.exists(TO_EXECUTE_FILE)

    # Write to the file
    with open(TO_EXECUTE_FILE, 'w') as f:
        f.writelines(["test\n", "hello\n"])

    # Reset the file again
    reset_to_execute()

    # Check that the file is empty
    with open(TO_EXECUTE_FILE, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 0
