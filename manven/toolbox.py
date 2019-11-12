from subprocess import check_output, CalledProcessError


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
