# coding: utf-8
from pathlib import Path
import os

ENV_FILE_NAME = "SAPPORO-service.dev.env"
ENV_FILE_PATH = Path(__file__).absolute(
).parent.parent.joinpath(ENV_FILE_NAME)

DEFAULT_PARAMS = {
    "ENV": "development",
    "DEBUG": True,
    "TESTING": True,
    "SECRET_KEY": "dummy_secret_key",
    "APPLICATION_ROOT": "/",
    "JSON_AS_ASCII": False,
    "JSON_SORT_KEYS": True,
    "JSONIFY_PRETTYPRINT_REGULAR": True,
}

ENV_PARAMS = list(DEFAULT_PARAMS.keys())


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8002


def load_os_env(param_key):
    if os.environ.get(param_key) is not None:
        return os.environ.get(param_key).strip('"')

    return None


def load_env_file(param_key):
    with ENV_FILE_PATH.open(mode="r") as r:
        for row in r.read().split("\n"):
            if not row:
                continue
            l_item = row.split("=")
            if len(l_item) <= 1:
                continue
            elif len(l_item) == 2:
                key, value = l_item
            else:
                key = l_item[0]
                value = "=".join(l_item[1:])
            if key == param_key:
                return value

    return None


def load_default_params(param_key):
    if param_key in DEFAULT_PARAMS:
        return DEFAULT_PARAMS[param_key]

    return None


def value_type_conversion(value):
    if value == "True":
        return True
    if value == "False":
        return False
    try:
        value = int(value)
    except ValueError:
        pass
    except TypeError:
        pass

    return value


def return_env_dict():
    env_dict = dict()
    for env_param in ENV_PARAMS:
        env_dict[env_param] = None
    for key, value in env_dict.items():
        if value is None:
            env_dict[key] = value_type_conversion(load_os_env(key))
    for key, value in env_dict.items():
        if value is None:
            env_dict[key] = value_type_conversion(load_env_file(key))
    for key, value in env_dict.items():
        if value is None:
            env_dict[key] = value_type_conversion(load_default_params(key))

    return env_dict


def return_host_port():
    host = None
    port = None
    if host is None:
        host = value_type_conversion(load_os_env("HOST"))
    if host is None:
        host = value_type_conversion(load_env_file("HOST"))
    if host is None:
        host = value_type_conversion(DEFAULT_HOST)
    if port is None:
        port = value_type_conversion(load_os_env("PORT"))
    if port is None:
        port = value_type_conversion(load_env_file("PORT"))
    if port is None:
        port = value_type_conversion(DEFAULT_PORT)

    return host, port


d_config = return_env_dict()
host, port = return_host_port()
