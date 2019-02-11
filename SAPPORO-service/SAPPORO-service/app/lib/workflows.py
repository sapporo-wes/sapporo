# coding: utf-8
from pathlib import Path

import requests
from flask import abort

from .util import WORKFLOW_INFO_FILE_PATH, read_workflow_info


def read_workflow_setting_file():
    workflow_info = read_workflow_info()
    data = dict()
    data["workflows"] = []
    for workflow in workflow_info["workflows"]:
        workflow["workflow_content"] = fetch_file(
            workflow["workflow_location"])
        workflow["workflow_parameters_template"] = fetch_file(
            workflow["workflow_parameters_template_location"])
        data["workflows"].append(workflow)

    return data

def fetch_file(url):
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        abort(400, "Can not get file: {}".format(url))
    return response.content.decode()
