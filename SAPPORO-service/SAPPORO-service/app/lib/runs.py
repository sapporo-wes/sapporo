# coding: utf-8
import os
import shlex
import signal
from datetime import datetime
from subprocess import PIPE, Popen
from time import sleep
from uuid import uuid4

import yaml
from flask import abort

from .util import SERVICE_BASE_DIR, read_service_info, read_workflow_info
from .workflows import fetch_file

RUN_BASE_DIR = SERVICE_BASE_DIR.joinpath("run")
RUN_ORDER_FILE_NAME = "run_order.yml"
WORKFLOW_FILE_NAME = "workflow"
WORKFLOW_PARAMETERS_FILE_NAME = "workflow_parameters"
STATUS_FILE_NAME = "status.txt"
PID_INFO_FILE_NAME = "run.pid"
UPLOAD_URL_FILE_NAME = "upload_url.txt"
STDOUT_FILE_NAME = "stdout.log"
STDERR_FILE_NAME = "stderr.log"
POST_REQUEST_REQUIRED_PARAMETERS = ["workflow_parameters",
                                    "workflow_name",
                                    "execution_engine_name"]
RUN_EXECUTION_SCRIPT_PATH = SERVICE_BASE_DIR.joinpath(
    "SAPPORO-service").joinpath("run_workflow.sh")


def validate_and_format_post_runs_request(request):
    """
    parameters = {
        "workflow_name": str,
        "workflow_location": str,
        "workflow_version": str,
        "workflow_content": str,
        "workflow_parameters": str,
        "language_type": str,
        "language_version": str,
        "execution_engine_name": str,
        "execution_engine_version": str,
        "start_time": str (datetime -> str),
        "end_time": str (datetime -> str),
    }
    """
    run_order = dict(request.form)
    run_order["workflow_parameters"] = request.files["workflow_parameters"].stream.read(
    ).decode("utf-8")
    for param in POST_REQUEST_REQUIRED_PARAMETERS:
        if param not in run_order.keys():
            abort(400, "Param: {} is not included.".format(param))
    workflow_location, workflow_version, workflow_content, language_type, language_version = fetch_workflow_file(
        run_order["workflow_name"])
    execution_engine_version = validate_engine(
        run_order["execution_engine_name"], language_type, language_version)
    run_order["workflow_location"] = workflow_location
    run_order["workflow_version"] = workflow_version
    run_order["workflow_content"] = workflow_content
    run_order["language_type"] = language_type
    run_order["language_version"] = language_version
    run_order["execution_engine_version"] = execution_engine_version
    run_order["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_order["end_time"] = ""

    return run_order


def fetch_workflow_file(workflow_name):
    workflow_info = read_workflow_info()
    for workflow in workflow_info["workflows"]:
        if workflow["workflow_name"] == workflow_name:
            workflow_content = fetch_file(workflow["workflow_location"])
            return workflow["workflow_location"], workflow["workflow_version"], workflow_content, workflow["language_type"], workflow["language_version"]
    abort(400, "Workflow does not exist: {}".format(workflow_name))


def validate_engine(engine, language_type, language_version):
    service_info = read_service_info()
    for workflow_engine in service_info["workflow_engines"]:
        if workflow_engine["engine_name"] == engine:
            for type_version in workflow_engine["workflow_types"]:
                if type_version["language_type"] == language_type and type_version["language_version"] == language_version:
                    return workflow_engine["engine_version"]
    abort(400, "Workflow engine parameter is incorrect.")


def execute(run_order):
    uuid = str(uuid4())
    prepare_run_dir(uuid, run_order)
    fork_run(uuid)

    return {"run_id": uuid, "status": "PENDING"}


def prepare_run_dir(uuid, run_order):
    run_dir = RUN_BASE_DIR.joinpath(uuid[:2]).joinpath(uuid)
    run_dir.mkdir(parents=True)
    with run_dir.joinpath(STATUS_FILE_NAME).open(mode="w") as f:
        f.write("QUEUED")
    with run_dir.joinpath(RUN_ORDER_FILE_NAME).open(mode="w") as f:
        f.write(yaml.dump(run_order, default_flow_style=False))
    with run_dir.joinpath(WORKFLOW_FILE_NAME).open(mode="w") as f:
        f.write(run_order["workflow_content"])
    with run_dir.joinpath(WORKFLOW_PARAMETERS_FILE_NAME).open(mode="w") as f:
        f.write(run_order["workflow_parameters"])
    run_dir.joinpath(PID_INFO_FILE_NAME).touch()
    run_dir.joinpath(UPLOAD_URL_FILE_NAME).touch()
    run_dir.joinpath(STDOUT_FILE_NAME).touch()
    run_dir.joinpath(STDERR_FILE_NAME).touch()

    return True


def fork_run(uuid):
    cmd = "sh {} {}".format(RUN_EXECUTION_SCRIPT_PATH, uuid)
    l_cmd = shlex.split(cmd)
    proc = Popen(l_cmd)
    run_dir = RUN_BASE_DIR.joinpath(uuid[:2]).joinpath(uuid)
    with run_dir.joinpath(PID_INFO_FILE_NAME).open(mode="w") as f:
        f.write(str(proc.pid))


def get_run_status_list():
    run_status_list = []
    for status_file in RUN_BASE_DIR.glob("**/{}".format(STATUS_FILE_NAME)):
        run_status = dict()
        run_status["run_id"] = status_file.parent.name
        update_end_time(run_status["run_id"])
        with status_file.open(mode="r") as f:
            run_status["status"] = f.read().strip()
        run_status_list.append(run_status)

    return run_status_list


def get_run_info(run_id):
    update_end_time(run_id)
    run_info = dict()
    run_info["run_id"] = run_id
    run_dir = list(RUN_BASE_DIR.glob("**/{}".format(run_id)))[0]
    with run_dir.joinpath(STATUS_FILE_NAME).open(mode="r") as f:
        run_info["status"] = f.read().strip()
    with run_dir.joinpath(RUN_ORDER_FILE_NAME).open(mode="r") as f:
        run_order = yaml.load(f)
        run_info.update(run_order)
    with run_dir.joinpath(UPLOAD_URL_FILE_NAME).open(mode="r") as f:
        run_info["upload_url"] = f.read().strip()
    with run_dir.joinpath(STDOUT_FILE_NAME).open(mode="r") as f:
        run_info["stdout"] = f.read()
    with run_dir.joinpath(STDERR_FILE_NAME).open(mode="r") as f:
        run_info["stderr"] = f.read()

    return run_info


def update_end_time(run_id):
    run_dir = list(RUN_BASE_DIR.glob("**/{}".format(run_id)))[0]
    status_file = run_dir.joinpath(STATUS_FILE_NAME)
    with status_file.open(mode="r") as f:
        run_status = f.read().strip()
    if run_status not in ["QUEUED", "RUNNING"]:
        end_time = datetime.fromtimestamp(
            status_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    else:
        return False
    with run_dir.joinpath(RUN_ORDER_FILE_NAME).open(mode="r") as f:
        run_order = yaml.load(f)
        run_order["end_time"] = end_time
    with run_dir.joinpath(RUN_ORDER_FILE_NAME).open(mode="w") as f:
        f.write(yaml.dump(run_order, default_flow_style=False))

    return True


def cancel_run(run_id):
    run_dir = list(RUN_BASE_DIR.glob("**/{}".format(run_id)))[0]
    status_file = run_dir.joinpath(STATUS_FILE_NAME)
    with status_file.open(mode="r") as f:
        run_status = f.read().strip()
        if run_status not in ["QUEUED", "RUNNING"]:
            abort(400, "The run can not be canceled.")
    with run_dir.joinpath(PID_INFO_FILE_NAME).open(mode="r") as f:
        pid = int(f.read().strip())
    ps = Popen(["ps", "aux"], stdout=PIPE).communicate()[0]
    processes = ps.decode("utf-8").split("\n")
    for process in processes:
        try:
            ps_pid = int(process.split()[0])
            l_command = process.split()[3:]
        except:
            continue
        if ps_pid == pid:
            if "sh" in l_command and str(run_id) in l_command:
                os.kill(pid, signal.SIGUSR1)
                with status_file.open(mode="w") as f:
                    f.write("CANCELED")
                return {"run_id": run_id, "status": "CANCELED"}
    abort(400, "There is no run to cancel.")
