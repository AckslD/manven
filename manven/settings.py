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
        "DEFAULT_PKGS": ["manven"],
    }


def _parse_default_pkgs(default_pkgs):
    if isinstance(default_pkgs, list):
        pass
    elif isinstance(default_pkgs, str):
        default_pkgs = default_pkgs.lstrip('[').rstrip(']')
        default_pkgs = default_pkgs.split(',')
        default_pkgs = [pkg.strip() for pkg in default_pkgs]
    else:
        raise TypeError(f"Unsupported type for, {type(default_pkgs)}, default_pkgs")
    return default_pkgs


_config_functions = [
    _config_from_cwd,
    _config_from_home,
    _config_from_dot_config,
    _config_from_defaults,
]


_config = _get_config()
_default_conf = _config_from_defaults()
for setting, default in _default_conf.items():
    if setting not in _config:
        raise RuntimeError(f"The entry '{setting}' must be in a configuration file")
ENVS_PATH = os.path.expanduser(_config["ENVS_PATH"])
DEFAULT_PKGS = _parse_default_pkgs(_config["DEFAULT_PKGS"])
