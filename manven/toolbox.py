import os
from subprocess import check_output, CalledProcessError

from manven.settings import ENVS_PATH


def has_binary(binary_name):
    """
    Checks if a given binary is in the PATH.

    This is done by checking what ``which binary_name`` returns.

    Args:
        binary_name (str): The name of the binary.

    Returns:
        bool: Whether the binary is in the PATH.
    """
    try:
        check_output(["which", binary_name])
    except CalledProcessError:
        return False
    else:
        return True


def has_virtualenv():
    """
    Checks if virtualenv is installed.

    Returns:
        bool: Whether the virtualenv is installed.
    """
    return has_binary("virtualenv")


def current_env():
    """
    Returns the current activated virtualenv.

    Returns:
        str or None: This is done by checking the environment variable VIRTUAL_ENV.
    """
    virtual_env = os.environ.get('VIRTUAL_ENV')
    if virtual_env is None:
        return None
    return os.path.relpath(virtual_env, ENVS_PATH)


def is_current_temp():
    """
    Checks if the current environment is a temporary environment.

    Returns:
        bool: True if the current environment is a temporary one.
    """

    current = current_env()
    if current is None:
        return False
    return current.startswith(".temp/")
