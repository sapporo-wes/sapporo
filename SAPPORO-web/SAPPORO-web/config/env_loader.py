# coding: utf-8
from pathlib import Path
import os

ENV_PARAMS = ["SAPPORO_web_HOST", "SAPPORO_web_PORT", "SAPPORO_web_DEBUG",
              "SAPPORO_web_LANGUAGE_CODE", "SAPPORO_web_TIME_ZONE", "SAPPORO_web_SECRET_KEY"]

ENV_FILE_NAME = "SAPPORO-web.dev.env"
ENV_FILE_PATH = Path(__file__).absolute(
).parent.parent.parent.joinpath(ENV_FILE_NAME)

DEFAULT_PARAMS = {
    "SAPPORO_web_HOST": "0.0.0.0",
    "SAPPORO_web_PORT": "8001",
    "SAPPORO_web_DEBUG": "True",
    "SAPPORO_web_LANGUAGE_CODE": "en",
    "SAPPORO_web_TIME_ZONE": "Asia/Tokyo",
    "SAPPORO_web_SECRET_KEY": "a)4r0@mbs6&yef62h2b4(h&b37f$ijn9t53t=hg5wk0_s#fm3e",
}


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


def return_env_dict():
    env_dict = dict()
    for env_param in ENV_PARAMS:
        env_dict[env_param] = None
    for key, value in env_dict.items():
        if value is None:
            env_dict[key] = load_os_env(key)
    for key, value in env_dict.items():
        if value is None:
            env_dict[key] = load_env_file(key)
    for key, value in env_dict.items():
        if value is None:
            env_dict[key] = load_default_params(key)

    return env_dict
