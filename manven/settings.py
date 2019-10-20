import os
from configparser import ConfigParser

import manven


def _get_config():
    """
    Returns the config.

    Returns:
        dict: A dictionary containing the settings.
    """
    for config_function in _config_functions:
        config = config_function()
        if config is not None:
            return config

    raise RuntimeError("Something went wrong, didn't get any config")


def _config_from_cwd():
    file_path = os.path.join(os.getcwd(), f".{manven.__name__}.conf")
    return _load_config(file_path)


def _config_from_home():
    file_path = os.path.expanduser(f"~/.{manven.__name__}.conf")
    return _load_config(file_path)


def _config_from_dot_config():
    file_path = os.path.expanduser(f"~/.config/{manven.__name__}/{manven.__name__}.conf")
    return _load_config(file_path)


def _load_config(file_path):
    if os.path.exists(file_path):
        cfg = ConfigParser()
        cfg.read(file_path)
        if 'manven' not in cfg:
            raise RuntimeError("A config file must have a section ['manven'].")
        return cfg['manven']
    else:
        return None


def _config_from_defaults():
    return {
        "ENVS_PATH": "~/venvs",
    }


_config_functions = [
    _config_from_cwd,
    _config_from_home,
    _config_from_dot_config,
    _config_from_defaults,
]


_config = _get_config()
if 'ENVS_PATH' not in _config:
    raise RuntimeError("The entry 'ENVS_PATH' must be in a configuration file")
ENVS_PATH = os.path.expanduser(_config["ENVS_PATH"])
