# coding: utf-8
from flask import Blueprint, jsonify, request

from .lib.runs import cancel_run, execute, get_run_info, get_run_status_list
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


# curl -X POST localhost:8002/runs/317c8109-e259-4b31-9bfd-581a3170ae7a/cancel
# curl -X POST localhost:8002/runs/92504da8-9858-4ce5-b445-6e63c9f4be96/cancel
@bp_app.route("/runs/<uuid:run_id>/cancel", methods=["POST"])
def post_runs_cancel(run_id):
    data = cancel_run(run_id)
    response = jsonify(data)
    response.status_code = 200
    return response
