# coding: utf-8
from copy import copy
from json import dumps
from uuid import uuid4
import shlex
from subprocess import Popen

from .util import SERVICE_BASE_DIR, read_service_info, read_workflow_info
from .workflows import resolve_workflow_file_path

RUN_BASE_DIR = SERVICE_BASE_DIR.joinpath("run")
STATUS_FILE_NAME = "state.txt"
RUN_ORDER_FILE_NAME = "run_order.json"
RUN_INFO_FILE_NAME = "run_info.json"
PID_INFO_FILE_NAME = "run.pid"
POST_REQUEST_REQUIRED_PARAMETERS = ["run_order",
                                    "workflow_name",
                                    "workflow_engine"]
RUN_EXECUTION_SCRIPT_PATH = SERVICE_BASE_DIR.joinpath(
    "SAPPORO-service").joinpath("run_workflow.sh")

service_info = read_service_info()
workflow_info = read_workflow_info()


def execute(parameters):
    if validate_post_parameters(parameters) is False:
        return None
    workflow_type, workflow_version, workflow_location = confirm_exist_workflow(
        parameters["workflow_name"])
    workflow_location = resolve_workflow_file_path(workflow_location)
    if workflow_location is None:
        return None
    if validate_engine(parameters["workflow_engine"], workflow_type, workflow_version) is False:
        return None
    uuid = str(uuid4())
    prepare_run_dir(uuid, parameters)
    fork_run(uuid)

    return uuid


def validate_post_parameters(parameters):
    for param in POST_REQUEST_REQUIRED_PARAMETERS:
        if param not in parameters.keys():
            return False

    return True


def confirm_exist_workflow(workflow_name):
    for workflow in workflow_info["workflows"]:
        if workflow["name"] == workflow_name:
            return workflow["type"], workflow["version"], workflow["location"]

    return None, None, None


def validate_engine(engine, workflow_type, workflow_version):
    for workflow_engine in service_info["workflow_engines"]:
        if workflow_engine["name"] == engine:
            for type_version in workflow_engine["workflow_types"]:
                if type_version["type"] == workflow_type and type_version["version"] == workflow_version:
                    return True

    return False


def prepare_run_dir(uuid, parameters):
    run_dir = RUN_BASE_DIR.joinpath(uuid[:2]).joinpath(uuid)
    run_dir.mkdir(parents=True)
    with run_dir.joinpath(STATUS_FILE_NAME).open(mode="w") as f:
        f.write("PENDING")
    with run_dir.joinpath(RUN_ORDER_FILE_NAME).open(mode="w") as f:
        f.write(parameters["run_order"].stream.read().decode("utf-8"))
        f.write("\n")
    with run_dir.joinpath(RUN_INFO_FILE_NAME).open(mode="w") as f:
        write_parameters = copy(parameters)
        del write_parameters["run_order"]
        f.write(dumps(write_parameters, ensure_ascii=False, indent=4))
        f.write("\n")


def fork_run(uuid):
    cmd = "bash {} {}".format(RUN_EXECUTION_SCRIPT_PATH, uuid)
    l_cmd = shlex.split(cmd)
    proc = Popen(l_cmd)
    run_dir = RUN_BASE_DIR.joinpath(uuid[:2]).joinpath(uuid)
    with run_dir.joinpath(PID_INFO_FILE_NAME).open(mode="w") as f:
        f.write(str(proc.pid))
