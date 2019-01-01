# coding: utf-8
import yaml
from ..util import SERVICE_BASE_DIR

SETTING_FILE_PATH = SERVICE_BASE_DIR.joinpath("service-info.yml")


def read_setting_file():
    with SETTING_FILE_PATH.open(mode="r") as f:
        data = yaml.load(f)

    return data
