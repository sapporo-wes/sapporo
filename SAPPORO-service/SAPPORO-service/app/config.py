# coding: utf-8
import os
import random
import string
from distutils.util import strtobool

APPLICATION_ROOT = "/"
JSON_AS_ASCII = False
JSON_SORT_KEYS = True
JSONIFY_PRETTYPRINT_REGULAR = True


def generate_d_config():
    d_config = dict()
    d_config["DEBUG"] = str2bool(os.environ.get("DEBUG"))
    if d_config["DEBUG"]:
        d_config["ENV"] = "development"
        d_config["TESTING"] = True
    else:
        d_config["ENV"] = "production"
        d_config["TESTING"] = False
    d_config["APPLICATION_ROOT"] = APPLICATION_ROOT
    d_config["JSON_AS_ASCII"] = JSON_AS_ASCII
    d_config["JSON_SORT_KEYS"] = JSON_SORT_KEYS
    d_config["JSONIFY_PRETTYPRINT_REGULAR"] = JSONIFY_PRETTYPRINT_REGULAR
    d_config["SECRET_KEY"] = generate_secret_key(16)

    return d_config


def str2bool(str):
    try:
        if strtobool(str):
            return True
        else:
            return False
    except ValueError:
        raise Exception(
            "Please check your docker-compose.yml:environment, The bool value should be 'true value are y, yes, t, true, on and 1; false values are n, no, f, false, off and 0'")


def generate_secret_key(n):
    c = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return "".join([random.choice(c) for i in range(n)])


d_config = generate_d_config()
ENABLE_GET_RUNS = str2bool(os.environ.get("ENABLE_GET_RUNS"))
