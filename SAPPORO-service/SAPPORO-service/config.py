# coding: utf-8
import os
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE_NAME = "SAPPORO-service.dev.env"
ENV_FILE_PATH = Path(__file__).absolute(
).parent.parent.joinpath(ENV_FILE_NAME)
load_dotenv(dotenv_path=ENV_FILE_PATH)

PARAMS = [
    "ENV",
    "DEBUG",
    "TESTING",
    "SECRET_KEY",
    "APPLICATION_ROOT",
    "JSON_AS_ASCII",
    "JSON_SORT_KEYS",
    "JSONIFY_PRETTYPRINT_REGULAR",
]


def generate_d_config():
    d_config = dict()
    for param in PARAMS:
        d_config[param] = os.environ.get(param)

    return d_config


d_config = generate_d_config()
host = os.environ.get("DEFAULT_HOST")
port = os.environ.get("DEFAULT_PORT")
