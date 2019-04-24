# coding: utf-8
from flask import Blueprint, abort, jsonify, request

from .config import ENABLE_GET_RUNS, d_config
from .lib.runs import (cancel_run, execute, get_run_info, get_run_status_list,
                       validate_and_format_post_runs_request)
from .lib.util import read_service_info
from .lib.workflows import read_workflow_setting_file
from .util import token_auth

bp_app = Blueprint("app", __name__)


# curl -X GET localhost:8002/service-info
@bp_app.route("/service-info", methods=["GET"])
@token_auth
def get_service_info():
    data = read_service_info()
    response = jsonify(data)
    response.status_code = 200
    return response


# curl -X GET localhost:8002/workflows
@bp_app.route("/workflows", methods=["GET"])
@token_auth
def get_workflows_list():
    data = read_workflow_setting_file()
    response = jsonify(data)
    response.status_code = 200
    return response


# curl -X GET localhost:8002/runs
@bp_app.route("/runs", methods=["GET"])
@token_auth
def get_runs():
    if ENABLE_GET_RUNS:
        data = get_run_status_list()
        response = jsonify(data)
        response.status_code = 200
        return response
    else:
        abort(403, "Forbidden")


# python3 ./tests/post_runs_mock/post_runs_mock_trim.py
@bp_app.route("/runs", methods=["POST"])
@token_auth
def post_runs():
    parameters = validate_and_format_post_runs_request(request)
    data = execute(parameters)
    response = jsonify(data)
    response.status_code = 201
    return response


# curl -X GET localhost:8002/runs/317c8109-e259-4b31-9bfd-581a3170ae7a
@bp_app.route("/runs/<uuid:run_id>", methods=["GET"])
@token_auth
def get_runs_uuid(run_id):
    data = get_run_info(run_id)
    response = jsonify(data)
    response.status_code = 200
    return response


# curl -X POST localhost:8002/runs/317c8109-e259-4b31-9bfd-581a3170ae7a/cancel
@bp_app.route("/runs/<uuid:run_id>/cancel", methods=["POST"])
@token_auth
def post_runs_cancel(run_id):
    data = cancel_run(run_id)
    response = jsonify(data)
    response.status_code = 201
    return response
