import os
import shutil
from subprocess import run
from itertools import count

from manven.toolbox import has_virtualenv
from manven.settings import ENVS_PATH


_path_to_here = os.path.dirname(os.path.abspath(__file__))
TO_EXECUTE_FILE = os.path.join(_path_to_here, ".to_execute.sh")


def create_environment(environment_name, *args, replace=False, no_manven=False, **virtualenv_ops):
    """
    Creates a (new if doesn't exist) environment with the given name.

    Args:
        environment_name (str): The name of the environment.
        replace (bool): Whether to replace an existing environment with the same name
            with a fresh one. (default: False)
        args, kwargs: Additional arguments passed to virtualenv.
    """
    # Check if virtualenv is installed and in the PATH
    if not has_virtualenv():
        raise SystemError("virtualenv is not installed or is not in the PATH")

    # Check if the environment already exists and if it should be replaced
    if _has_environment(environment_name):
        if replace:
            path_to_venv = _get_absolute_path(environment_name)
            shutil.rmtree(path_to_venv)
        else:
            return

    _create_an_environment(environment_name, ENVS_PATH, no_manven=no_manven, **virtualenv_ops)


def activate_environment(environment_name, basefolder=ENVS_PATH):
    """
    Activates an existing environment.

    Args:
        environment_name (str): The name of the environment.
        basefolder (str): The folder to contain the environment.
    """
    if not _has_environment(environment_name, basefolder=basefolder):
        raise ValueError("Environment {environment_name} does not exist")

    # Get the path to the activate script, based on the shell
    activate_script = _get_activate_script_path(environment_name, basefolder=basefolder)

    # Source the activate file
    args = ["source", activate_script]
    _write_execute_to_file(args)


def list_environments(include_temporary=False):
    """
    Returns a list of available environments.

    Args:
        include_temporary (bool): Whether to include temporary environments.
            (default False).

    Returns:
        list: list of str consisting of the names of the available environments
    """
    # Get the available environments
    if os.path.exists(ENVS_PATH):
        environments = sorted([venv for venv in os.listdir(ENVS_PATH) if _is_environment(venv)])
    else:
        environments = []

    # Optionally include the temporary environments
    if include_temporary:
        environments += [f".temp/{venv}" for venv in sorted(_list_temporary_environments())]

    return environments


def activate_temp_environment(no_manven=False):
    """
    Creates and activates a new temporary environment.
    """
    path_to_temp = _get_temp_path()
    temp_env_name = _get_unused_temp_name(path_to_temp)
    _create_an_environment(temp_env_name, path_to_temp, no_manven=no_manven)
    activate_environment(temp_env_name, basefolder=path_to_temp)


def prune_temp_environments():
    """Prunes all temporary environments."""
    path_to_temp = _get_temp_path()
    temp_environments = sorted(_list_temporary_environments())
    for temp_environment in temp_environments:
        _remove_file_or_folder(os.path.join(path_to_temp, temp_environment))


def remove_environment(environment_name):
    """
    Removes an existing environment.

    Args:
        environment_name (str): The name of the environment.
    """
    if _has_environment(environment_name):
        path_to_venv = _get_absolute_path(environment_name)
        shutil.rmtree(path_to_venv)


def deactivate_environment():
    """
    Deactivates the current environment (if there is one).
    """
    args = ["deactivate"]
    _write_execute_to_file(args)


def reset_to_execute():
    """
    Resets what commands that should be executed in the shell.
    """
    with open(TO_EXECUTE_FILE, 'w'):
        pass


def check_first_usage():
    """
    Checks if this is the first time manven is run and prints some information.
    """
    if not os.path.exists(TO_EXECUTE_FILE):
        input("It looks like it's the first time you're using manven.\n"
              "Next time you won't see this message.\n"
              "Since manven sometimes needs to source certain files, "
              "it is recommended that you add the following alias to your system:\n"
              "\n"
              "alias smanven='source $(which manven)'\n"
              "\n"
              "If you're using fish, add instead:\n"
              "\n"
              "alias smanven 'source (which manven.fish)'\n"
              "\n"
              "Press enter to continue...")


def _create_an_environment(environment_name, basefolder=ENVS_PATH, no_manven=False, **virtualenv_ops):
    """
    Creates a new environment with a given name in a given folder.

    Args:
        environment_name (str): The name of the environment.
        basefolder (str): The folder to contain the environment.
    """
    # Check that basefolder exists, otherwise create it
    if not os.path.exists(basefolder):
        os.makedirs(basefolder)

    # Create the new environment
    options = _format_options(virtualenv_ops)
    args = ["virtualenv", *options, environment_name]
    output = run(args, cwd=basefolder)

    # Check that the command worked
    message = f"Something went wrong when creating the environment {environment_name}"
    _assert_output(output, message)

    if not no_manven:
        _install_manven(environment_name, basefolder=basefolder)


def _format_options(virtualenv_ops):
    """Formats the a dictionary of options to be passed as flags to virtualenv."""
    options = []
    for option_name, option_value in virtualenv_ops.items():
        if option_value:  # If True or non-zero length string
            option = option_name.replace('_', '-')
            option = f"--{option}"
            if not isinstance(option_value, bool):  # If it's a True/False flag we simply add the flag, not the value
                option_value = option_value.replace('=', '')
                option += f"={option_value}"
            options.append(option)
    return options


def _install_manven(environment_name, basefolder=ENVS_PATH):
    """
    Installs manven.
    This is used so that manven can also be used in new environments.

    Args:
        environment_name (str): The name of the environment.
        basefolder (str): The folder to contain the environment.
    """
    pip = os.path.join(basefolder, environment_name, "bin", "pip")
    if not os.path.exists(pip):
        raise ValueError(f"Environment {environment_name} at {basefolder} does not exist.")

    args = [pip, "install", "manven"]
    output = run(args)

    # Check that the command worked
    message = "Something went wrong when installing manven"
    _assert_output(output, message)


def _write_execute_to_file(args):
    """Writes (w mode) commands to be executed to a file."""
    with open(TO_EXECUTE_FILE, 'w') as f:
        f.write(' '.join(args))


def _list_temporary_environments():
    """
    Returns a list of the current temporary environments.

    Returns:
        list: list of str consisting of the names of the temporary environments.
    """
    temp_path = _get_temp_path()
    if os.path.exists(temp_path):
        return [venv for venv in os.listdir(temp_path) if _is_environment(venv, basefolder=temp_path)]
    else:
        return []


def _is_environment(environment_name, basefolder=ENVS_PATH):
    """
    Checks if the environment name is an existing environment.

    This is done by checking if ``bin/activate`` exists in the folder.

    Args:
        environment_name (str): The name of the environment.
        basefolder (str): The folder to contain the environment.

    Returns:
        bool: If the environment exists.
    """
    activate_script = _get_activate_script_path(environment_name, basefolder=basefolder)

    return os.path.exists(activate_script)


def _assert_output(output, message):
    """
    Checks that the output from a subprocess.run call has 0 as return code.
    """
    if output.returncode != 0:
        raise RuntimeError(f"{message}: {output.stderr}")


def _get_activate_script_path(environment_name, basefolder=ENVS_PATH):
    """
    Gets the absolute path to the activate script for a given environment.


    Args:
        environment_name (str): The name of the environment.
        basefolder (str): The folder to contain the environment.

    Returns:
        bool: If the environment exists.
    """
    # Get the path to the activate script, based on the shell
    path_to_venv = _get_absolute_path(environment_name, basefolder=basefolder)
    activate_script = os.path.join(path_to_venv, "bin", _get_activate_script_name())
    return activate_script


def _get_activate_script_name():
    """
    Gets the name of the activate script based on what's the current shell is.

    Returns:
        str: The name of the file.
    """
    # Get the current shell
    shell = _get_current_shell()

    shell_to_script_name = {
        "sh": "activate",
        "bash": "activate",
        "zsh": "activate",
        "dash": "activate",
        "csh": "activate.csh",
        "fish": "activate.fish",
    }

    script_name = shell_to_script_name.get(shell)
    if script_name is None:
        raise ValueError("Unknown shell {shell}")

    return script_name


def _get_current_shell():
    """
    Returns the current shell set by the environment variable $SHELL.

    Returns:
        str: The name of the current shell.
    """
    return os.environ['SHELL'].split('/')[-1]


def _get_absolute_path(environment_name, basefolder=ENVS_PATH):
    """
    Gets the absolute path to where the environment folder should be,
    based on the user settings.

    Args:
        environment_name (str): The name of the environment.
        basefolder (str): The folder to contain the environment.
    """
    return os.path.join(basefolder, environment_name)


def _has_environment(environment_name, basefolder=ENVS_PATH):
    """
    Checks if the environment already exists.

    Args:
        environment_name (str): The name of the environment.
        basefolder (str): The folder to contain the environment.

    Returns:
        bool: Whether the environment exists.
    """
    path_to_venv = _get_absolute_path(environment_name, basefolder=basefolder)
    return os.path.exists(path_to_venv)


def _get_temp_path():
    """
    Returns the path to where the temporary environments are stored.

    Returns:
        str: The path
    """
    temp_path = os.path.join(ENVS_PATH, ".temp")

    # Create the path if it does not exist
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    return temp_path


def _get_unused_temp_name(path_to_temp):
    """
    Get a new unused name for a temporary environment.
    """
    # Find an unused name
    for i in count():
        temp_env_name = f"temp_venv_{i}"
        new_path = os.path.join(path_to_temp, temp_env_name)
        if not os.path.exists(new_path):
            return temp_env_name


def _remove_file_or_folder(path):
    """Effectively does ``rm -rf path``"""
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)
