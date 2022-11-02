import os
import shutil
from subprocess import run, check_output
from itertools import count

from manven.toolbox import has_virtualenv, current_env, is_current_temp
from manven.settings import ENVS_PATH, DEFAULT_PKGS, PIP_INSTALL_FLAGS

_path_to_here = os.path.dirname(os.path.abspath(__file__))
_to_execute_filename = ".to_execute.sh"
TO_EXECUTE_FILE = os.path.join(_path_to_here, _to_execute_filename)
_last_env_filename = ".last_env"
LAST_ENV = os.path.join(_path_to_here, _last_env_filename)


def create_environment(
    environment_name,
    replace=False,
    clone=None,
    default_pkgs=DEFAULT_PKGS,
    pip_install_flags=PIP_INSTALL_FLAGS,
    **virtualenv_ops
):
    """
    Creates a (new if doesn't exist) environment with the given name.

    Args:
        environment_name (str): The name of the environment.
        replace (bool): Whether to replace an existing environment with the same name
            with a fresh one. (default: False)
        clone (str, optional): Whether to clone from an existing environment instead of creating a new one.
        virtualenv_ops: Additional arguments passed to virtualenv.
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

    _create_an_environment(
        environment_name=environment_name,
        clone=clone,
        default_pkgs=default_pkgs,
        pip_install_flags=pip_install_flags,
        **virtualenv_ops
    )


def activate_environment(environment_name, basefolder=ENVS_PATH):
    """
    Activates an existing environment.

    Args:
        environment_name (str): The name of the environment.
        basefolder (str): The folder to contain the environment.
    """
    if not _has_environment(environment_name, basefolder=basefolder):
        raise ValueError(f"Environment {environment_name} does not exist")

    # Get the path to the activate script, based on the shell
    activate_script = _get_activate_script_path(environment_name, basefolder=basefolder)

    # Source the activate file
    args = ["source", activate_script]
    _write_execute_to_file(args)

    # Update last activated environment
    _update_last_activated_environment(environment_name, basefolder)


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


def activate_temp_environment(
    clone=None,
    basefolder=ENVS_PATH,
    default_pkgs=DEFAULT_PKGS,
    pip_install_flags=PIP_INSTALL_FLAGS,
    **virtualenv_ops,
):
    """
    Creates and activates a new temporary environment.
    """
    path_to_temp = _get_temp_path()
    temp_env_name = _get_unused_temp_name(path_to_temp)
    rel_temp_path = os.path.join(os.path.relpath(path_to_temp, start=basefolder), temp_env_name)
    _create_an_environment(
        environment_name=rel_temp_path,
        clone=clone,
        default_pkgs=default_pkgs,
        pip_install_flags=pip_install_flags,
        **virtualenv_ops
    )
    activate_environment(temp_env_name, basefolder=path_to_temp)


def prune_temp_environments():
    """Prunes all temporary environments."""
    if is_current_temp():
        raise RuntimeError("Cannot prune temporary environments when one is currently active ({})"
                           .format(current_env()))
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
    if current_env() == environment_name:
        raise ValueError("Cannot remove the currently activated environment.")
    if _has_environment(environment_name):
        path_to_venv = _get_absolute_path(environment_name)
        shutil.rmtree(path_to_venv)


def deactivate_environment():
    """
    Deactivates the current environment (if there is one).
    """
    args = ["deactivate"]
    _write_execute_to_file(args)


def open_last_environment():
    """
    Activates the last activated environment by writing to a file.
    """
    if not os.path.exists(LAST_ENV):
        print("No environment has been activated yet")
        return

    with open(LAST_ENV, 'r') as f:
        environment_name, basefolder = f.read().split('\n')
    activate_environment(environment_name, basefolder=basefolder)


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


def _create_an_environment(
    environment_name,
    clone=None,
    basefolder=ENVS_PATH,
    default_pkgs=DEFAULT_PKGS,
    pip_install_flags=None,
    **virtualenv_ops
):
    """
    Creates a new environment with a given name in a given folder.

    Args:
        environment_name (str): The name of the environment.
        clone (str, optional): Whether to clone from an existing environment instead of creating a new one.
        basefolder (str): The folder to contain the environment.
    """
    # Check that basefolder exists, otherwise create it
    if not os.path.exists(basefolder):
        os.makedirs(basefolder)

    if clone is not None:
        # Clone the environment
        args = ['virtualenv-clone', clone, environment_name]
    else:
        # Create the new environment
        options = _format_options(virtualenv_ops)
        args = ["virtualenv", *options, environment_name]
    _run_assert_output(args, f"Something went wrong when creating the environment {environment_name}", cwd=basefolder)

    if clone is None:
        _install_packages(
            environment_name,
            packages=default_pkgs,
            basefolder=basefolder,
            pip_install_flags=pip_install_flags,
        )


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


def _install_packages(environment_name, packages, basefolder=ENVS_PATH, pip_install_flags=None):
    """
    Installs packages to an environment.

    Args:
        environment_name (str): The name of the environment.
        packages (list): List of strings specifying python packages to install
        basefolder (str): The folder to contain the environment.
    """
    if not packages:
        return
    pip = os.path.join(basefolder, environment_name, "bin", "pip")
    if not os.path.exists(pip):
        raise ValueError(f"Environment {environment_name} at {basefolder} does not exist.")

    if pip_install_flags is None:
        pip_install_flags = []
    _run_assert_output(
        [pip, "install", *pip_install_flags, *packages],
        f"Something went wrong when installing {packages}",
    )

    if "manven" in packages:
        # Add the to execute file such that the first time text is not printed when using manven
        python = os.path.join(basefolder, environment_name, "bin", "python")
        args = [python, "-m", "manven"]
        output = check_output(args).decode('utf-8').strip()
        venv_to_execute_file = os.path.join(output, _to_execute_filename)
        _run_assert_output(
            ["touch", venv_to_execute_file],
            "Something went wrong when adding the file {}".format(TO_EXECUTE_FILE),
        )


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


def _update_last_activated_environment(environment_name, basefolder):
    """
    Updates the last activated environment by writing to a file.

    Args:
        environment_name (str): The name of the environment.
        basefolder (str): The folder to contain the environment.
    """
    with open(LAST_ENV, 'w') as f:
        f.write(f"{environment_name}\n{basefolder}")


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


def _run_assert_output(args, message, **kwargs):
    """
    Runs the commmand and checks that the output from a subprocess.run call has 0 as return code.
    """
    output = run(args, **kwargs)
    if output.returncode != 0:
        raise RuntimeError(f"{message}: (" + ' '.join(args) + ')')


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
    if 'SHELL' not in os.environ:
        # default to bash
        return 'bash'
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
