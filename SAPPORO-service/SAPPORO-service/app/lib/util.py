# coding: utf-8
from pathlib import Path

import yaml

SERVICE_BASE_DIR = Path(__file__).absolute(
).parent.parent.parent.parent
SERVICE_INFO_FILE_PATH = SERVICE_BASE_DIR.joinpath(
    "config").joinpath("service-info.yml")
WORKFLOW_INFO_FILE_PATH = SERVICE_BASE_DIR.joinpath(
    "config").joinpath("workflow-info.yml")
SUPPORTED_WES_VERSIONS = ["v1.0.0"]


def read_workflow_info():
    with WORKFLOW_INFO_FILE_PATH.open(mode="r") as f:
        return yaml.load(f)


def read_service_info():
    with SERVICE_INFO_FILE_PATH.open(mode="r") as f:
        data = yaml.load(f)
    data["supported_wes_versions"] = SUPPORTED_WES_VERSIONS
    return data
