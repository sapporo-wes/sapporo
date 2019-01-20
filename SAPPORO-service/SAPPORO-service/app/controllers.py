# coding: utf-8
from flask import Blueprint, abort, jsonify, request

from .lib.runs import execute, get_run_status_list
from .lib.util import read_service_info
from .lib.workflows import read_workflow_setting_file

bp_app = Blueprint("app", __name__)


# curl -X GET localhost:8002/service-info
@bp_app.route("/service-info", methods=["GET"])
def get_service_info():
    data = read_service_info()
    response = jsonify(data)
    response.status_code = 200
    return response


# curl -X GET localhost:8002/workflows
@bp_app.route("/workflows", methods=["GET"])
def get_workflows_list():
    data = read_workflow_setting_file()
    response = jsonify(data)
    response.status_code = 200
    return response


# curl -X GET localhost:8002/runs
@bp_app.route("/runs", methods=["GET"])
def get_run_status_list():
    data = get_run_status_list()
    response = jsonify(data)
    response.status_code = 200
    return response


# python3 ./tests/runs_post.py
@bp_app.route("/runs", methods=["POST"])
def post_runs():
    fields = [field for field in request.form]
    values = [request.form[field] for field in request.form]
    parameters = dict(zip(fields, values))
    parameters["run_order"] = request.files["run_order"]
    uuid = execute(parameters)
    if uuid is None:
        abort(400)
    response = jsonify({"run_id": uuid})
    response.status_code = 200
    return response
