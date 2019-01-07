# coding: utf-8
import yaml

from .util import WORKFLOW_BASE_DIR

WORKFLOW_SETTING_FILE_PATH = WORKFLOW_BASE_DIR.joinpath("workflow-info.yml")


def read_workflow_setting_file():
    with WORKFLOW_SETTING_FILE_PATH.open(mode="r") as f:
        data = yaml.load(f)

    return data
