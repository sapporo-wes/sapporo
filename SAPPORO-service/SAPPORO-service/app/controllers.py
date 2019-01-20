# coding: utf-8
from flask import Blueprint, jsonify, request

from .lib.runs import execute, get_run_status_list, get_run_info
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
def get_runs():
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
    data = execute(parameters)
    response = jsonify(data)
    response.status_code = 200
    return response


@bp_app.route("/runs/<uuid:run_id>", methods=["GET"])
def get_runs_uuid(run_id):
    data = get_run_info(run_id)
    response = jsonify(data)
    response.status_code = 200
    return response
