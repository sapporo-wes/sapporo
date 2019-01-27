# coding: utf-8
import shlex
from copy import copy
from json import dumps, loads
from subprocess import Popen, PIPE
from uuid import uuid4
import os
import signal

from flask import abort

from .util import SERVICE_BASE_DIR, read_service_info, read_workflow_info
from .workflows import resolve_workflow_file_path

RUN_BASE_DIR = SERVICE_BASE_DIR.joinpath("run")
STATUS_FILE_NAME = "state.txt"
RUN_ORDER_FILE_NAME = "run_order.json"
RUN_INFO_FILE_NAME = "run_info.json"
PID_INFO_FILE_NAME = "run.pid"
UPLOAD_URL_FILE_NAME = "upload_url.txt"
POST_REQUEST_REQUIRED_PARAMETERS = ["run_order",
                                    "workflow_name",
                                    "workflow_engine"]
RUN_EXECUTION_SCRIPT_PATH = SERVICE_BASE_DIR.joinpath(
    "SAPPORO-service").joinpath("run_workflow.sh")

service_info = read_service_info()
workflow_info = read_workflow_info()


def execute(parameters):
    validate_parameters(parameters)
    uuid = str(uuid4())
    prepare_run_dir(uuid, parameters)
    fork_run(uuid)

    return {"run_id": uuid}


def validate_parameters(parameters):
    for param in POST_REQUEST_REQUIRED_PARAMETERS:
        if param not in parameters.keys():
            abort(400, "Param: {} is not included.".format(param))
    workflow_type, workflow_version, workflow_location = confirm_exist_workflow(
        parameters["workflow_name"])
    validate_engine(parameters["workflow_engine"],
                    workflow_type, workflow_version)


def confirm_exist_workflow(workflow_name):
    for workflow in workflow_info["workflows"]:
        if workflow["name"] == workflow_name:
            workflow_location = resolve_workflow_file_path(
                workflow["location"])
            return workflow["type"], workflow["version"], workflow_location
    abort(400, "Workflow does not exist: {}".format(workflow_name))


def validate_engine(engine, workflow_type, workflow_version):
    for workflow_engine in service_info["workflow_engines"]:
        if workflow_engine["name"] == engine:
            for type_version in workflow_engine["workflow_types"]:
                if type_version["type"] == workflow_type and type_version["version"] == workflow_version:
                    return True
    abort(400, "Workflow engine parameter is incorrect.")


def prepare_run_dir(uuid, parameters):
    run_dir = RUN_BASE_DIR.joinpath(uuid[:2]).joinpath(uuid)
    run_dir.mkdir(parents=True)
    with run_dir.joinpath(STATUS_FILE_NAME).open(mode="w") as f:
        f.write("QUEUED")
    with run_dir.joinpath(RUN_ORDER_FILE_NAME).open(mode="w") as f:
        f.write(parameters["run_order"].stream.read().decode("utf-8"))
        f.write("\n")
    with run_dir.joinpath(RUN_INFO_FILE_NAME).open(mode="w") as f:
        write_parameters = copy(parameters)
        del write_parameters["run_order"]
        f.write(dumps(write_parameters, ensure_ascii=False, indent=4))
        f.write("\n")
    run_dir.joinpath("stdout.log").touch()
    run_dir.joinpath("stderr.log").touch()
    run_dir.joinpath(PID_INFO_FILE_NAME).touch()
    run_dir.joinpath(UPLOAD_URL_FILE_NAME).touch()


def fork_run(uuid):
    cmd = "bash {} {}".format(RUN_EXECUTION_SCRIPT_PATH, uuid)
    l_cmd = shlex.split(cmd)
    proc = Popen(l_cmd)
    run_dir = RUN_BASE_DIR.joinpath(uuid[:2]).joinpath(uuid)
    with run_dir.joinpath(PID_INFO_FILE_NAME).open(mode="w") as f:
        f.write(str(proc.pid))


def get_run_status_list():
    run_state_list = []
    for status_file in RUN_BASE_DIR.glob("**/{}".format(STATUS_FILE_NAME)):
        run_state = dict()
        run_state["run_id"] = status_file.parent.name
        with status_file.open(mode="r") as f:
            run_state["status"] = f.read().strip()
        run_state_list.append(run_state)

    return run_state_list


def get_run_info(run_id):
    run_info = dict()
    run_dir = list(RUN_BASE_DIR.glob("**/{}".format(run_id)))[0]
    run_info["run_id"] = run_dir.name
    with run_dir.joinpath(STATUS_FILE_NAME).open(mode="r") as f:
        run_info["status"] = f.read().strip()
    with run_dir.joinpath(RUN_INFO_FILE_NAME).open(mode="r") as f:
        d_info = loads(f.read())
        run_info["workflow_name"] = d_info["workflow_name"]
        run_info["workflow_engine"] = d_info["workflow_engine"]
    with run_dir.joinpath(RUN_ORDER_FILE_NAME).open(mode="r") as f:
        run_info["run_order"] = f.read()
    with run_dir.joinpath(UPLOAD_URL_FILE_NAME).open(mode="r") as f:
        run_info["upload_url"] = f.read().strip()
    with run_dir.joinpath("stdout.log").open(mode="r") as f:
        run_info["stdout"] = f.read()
    with run_dir.joinpath("stderr.log").open(mode="r") as f:
        run_info["stderr"] = f.read()

    return run_info


def cancel_run(run_id):
    run_dir = list(RUN_BASE_DIR.glob("**/{}".format(run_id)))[0]
    with run_dir.joinpath(STATUS_FILE_NAME).open(mode="r") as f:
        status = f.read().strip()
        if status not in ["QUEUED", "RUNNING"]:
            abort(400, "The run can not be canceled.")
    with run_dir.joinpath(PID_INFO_FILE_NAME).open(mode="r") as f:
        pid = int(f.read().strip())
    ps = Popen(["ps", "aux"], stdout=PIPE).communicate()[0]
    processes = ps.decode("utf-8").split("\n")
    for process in processes:
        try:
            ps_pid = int(process.split[1])
            l_command = process.split()[10:]
        except:
            continue
        if ps_pid == pid:
            if "bash" in l_command and str(run_id) in l_command:
                os.kill(pid, signal.SIGKILL)
                with run_dir.joinpath(STATUS_FILE_NAME).open(mode="w") as f:
                    f.write("CANCELED")
                return {"run_id": run_id}
    abort(400, "There is no run to cancel.")
