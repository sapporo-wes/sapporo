# coding: utf-8
from pathlib import Path
import os

from dotenv import load_dotenv

ENV_FILE_NAME = "SAPPORO-web.dev.env"
ENV_FILE_PATH = Path(__file__).absolute(
).parent.parent.parent.joinpath(ENV_FILE_NAME)
load_dotenv(dotenv_path=ENV_FILE_PATH)

PARAMS = [
    "SAPPORO_web_HOST",
    "SAPPORO_web_PORT",
    "SAPPORO_web_DEBUG",
    "SAPPORO_web_LANGUAGE_CODE",
    "SAPPORO_web_TIME_ZONE",
    "SAPPORO_web_SECRET_KEY"
]


def generate_d_config():
    d_config = dict()
    for param in PARAMS:
        d_config[param] = os.environ.get(param)

    return d_config


d_config = generate_d_config()
