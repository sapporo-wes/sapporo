# coding: utf-8
from pathlib import Path

from .util import WORKFLOW_INFO_FILE_PATH, read_workflow_info


def read_workflow_setting_file():
    workflow_info = read_workflow_info()
    data = dict()
    data["workflows"] = []
    for workflow in workflow_info["workflows"]:
        workflow_location = resolve_workflow_file_path(
            workflow["workflow_location"])
        run_order_template_location = resolve_workflow_file_path(
            workflow["run_order_template_location"])
        del workflow["workflow_location"]
        del workflow["run_order_template_location"]
        with workflow_location.open(mode="r") as f:
            workflow["content"] = f.read()
        with run_order_template_location.open(mode="r") as f:
            workflow["run_order_template"] = f.read()
        data["workflows"].append(workflow)

    return data


def resolve_workflow_file_path(location):
    if location[0] == "/":
        path = Path(location).absolute()
    elif location[0] == ".":
        path = WORKFLOW_INFO_FILE_PATH.parent.joinpath(location).absolute()
    else:
        path = WORKFLOW_INFO_FILE_PATH.parent.joinpath(location).absolute()
    assert path.exists() is True, "File does not exist, Check workflow-info.yml: {}".format(location)
    assert path.is_dir() is False, "Location is Dir, Check workflow-info.yml: {}".format(location)

    return path
