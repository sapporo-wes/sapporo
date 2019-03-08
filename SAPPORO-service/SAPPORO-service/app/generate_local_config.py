# coding: utf-8
import secrets
from pathlib import Path


CONFIG_FILE_NAME = "local_config.py"
CONFIG_FILE_PATH = Path(__file__).absolute().parent.joinpath(CONFIG_FILE_NAME)


def generate_secret_key():
    with CONFIG_FILE_PATH.open(mode="w") as f:
        f.write('SECRET_KEY = "{}"\n'.format(secrets.token_urlsafe(32)))


if __name__ == "__main__":
    if CONFIG_FILE_PATH.exists() is False:
        generate_secret_key()
