# coding: utf-8
from copy import copy
from json import dumps
from uuid import uuid4
import shlex
from subprocess import Popen

from .util import RUN_BASE_DIR, WORKFLOW_BASE_DIR

WORKFLOW_DIR_PATH = WORKFLOW_BASE_DIR.joinpath("workflow")
RUN_ORDER_FILE_NAME = "run-order.json"
RUN_INFO_FILE_NAME = "run-info.json"
PID_INFO_FILE_NAME = "run.pid"
STATUS_FILE_NAME = "state.txt"
POST_REQUEST_REQUIRED_PARAMETERS = ["parameters",
                                    "name",
                                    "engine",
                                    "type",
                                    "version"]
RUN_EXECUTION_SCRIPT_PATH = RUN_BASE_DIR.joinpath("run.sh")


def execute_run(data):
    if validate_post_data(data) is False:
        return None
    if exist_workflow(data["name"], data["type"]) is False:
        return None
    uuid = str(uuid4())
    run_dir = RUN_BASE_DIR.joinpath(uuid)
    run_dir.mkdir()
    with run_dir.joinpath(STATUS_FILE_NAME).open(mode="w") as f:
        f.write("PENDING")
    with run_dir.joinpath(RUN_ORDER_FILE_NAME).open(mode="w") as f:
        f.write(data["parameters"])
    with run_dir.joinpath(RUN_INFO_FILE_NAME).open(mode="w") as f:
        write_data = copy(data)
        del write_data["parameters"]
        f.write(dumps(write_data))
    fork_run(uuid)

    return uuid


def validate_post_data(data):
    for param in POST_REQUEST_REQUIRED_PARAMETERS:
        if param not in data.keys():
            return False

    return True


def exist_workflow(name, type):
    if type == "CWL":
        ext = "cwl"
    elif type == "WDL":
        ext = "wdl"
    elif type == "Nextflow":
        ext = "nf"
    else:
        return False
    workflow_file_path = WORKFLOW_DIR_PATH.joinpath("{}.{}".format(name, ext))
    if workflow_file_path.exists() is False:
        return False

    return True


def fork_run(uuid):
    cmd = "bash {} {}".format(RUN_EXECUTION_SCRIPT_PATH, uuid)
    l_cmd = shlex.split(cmd)
    proc = Popen(l_cmd)
    with RUN_BASE_DIR.joinpath(uuid).joinpath(PID_INFO_FILE_NAME).open(mode="w") as f:
        f.write(str(proc.pid))


"""
curl -X POST "localhost:8002/runs" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "parameters=param" -F "type=CWL" -F "version=v1.0" -F "engine=cwltool" -F "name=test-workflow"
"""
