# coding: utf-8
from pathlib import Path

import yaml

SERVICE_BASE_DIR = Path(__file__).absolute(
).parent.parent.parent.parent
SERVICE_INFO_FILE_PATH = SERVICE_BASE_DIR.joinpath("service-info.yml")
WORKFLOW_INFO_FILE_PATH = SERVICE_BASE_DIR.joinpath("workflow-info.yml")


def read_workflow_info():
    with WORKFLOW_INFO_FILE_PATH.open(mode="r") as f:
        return yaml.load(f)


def read_service_info():
    with SERVICE_INFO_FILE_PATH.open(mode="r") as f:
        return yaml.load(f)
