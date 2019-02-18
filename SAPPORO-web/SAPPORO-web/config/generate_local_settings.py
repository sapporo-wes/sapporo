# coding: utf-8
import secrets
from pathlib import Path


with Path(__file__).absolute().parent.joinpath("local_settings.py").open(mode="w") as f:
    f.write('SECRET_KEY = "{}"\n'.format(secrets.token_urlsafe(32)))
