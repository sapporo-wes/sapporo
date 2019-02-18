# coding: utf-8
from flask import Blueprint, current_app, jsonify, request, abort

from .config import ENABLE_GET_RUNS, TOKEN_AUTH, d_config
from .lib.runs import (cancel_run, execute, get_run_info, get_run_state_list,
                       validate_and_format_post_runs_request)
from .lib.util import read_service_info, SERVICE_BASE_DIR
from .lib.workflows import read_workflow_setting_file
from secrets import compare_digest

bp_app = Blueprint("app", __name__)


if d_config["DEBUG"] is False:
    @bp_app.errorhandler(400)
    @bp_app.errorhandler(401)
    @bp_app.errorhandler(403)
    @bp_app.errorhandler(404)
    @bp_app.errorhandler(500)
    def error_handler(error):
        response = {
            "msg": error.description,
            "status_code": error.code,
        }
        response = jsonify(response)
        response.status_code = error.code
        return response

    @bp_app.errorhandler(Exception)
    def error_handler_exception(exception):
        import traceback
        current_app.logger.error(exception.args[0])
        traceback.print_exc()
        response = {
            "msg": "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.: {}".format(exception.args[0]),
            "status_code": 500,
        }
        response = jsonify(response)
        response.status_code = 500
        return response


def token_auth(func):
    def wrapper(*args, **kwargs):
        if TOKEN_AUTH:
            token_list = SERVICE_BASE_DIR.joinpath(
                "config").joinpath("token_list.txt")
            if token_list.exists() is False:
                abort(400, "token_list.txt not found.")
            request_token = request.headers.get("Authorization", None)
            if request_token is None:
                abort(401, "Authorization Header does not exist.")
            b_auth = False
            with token_list.open(mode="r") as f:
                for token in f.read().split("\n"):
                    if token == "":
                        continue
                    if compare_digest(token, request_token):
                        b_auth = True
            if b_auth is False:
                abort(401, "Authorization Token is incorrect.")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__

    return wrapper


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


if ENABLE_GET_RUNS:
    # curl -X GET localhost:8002/runs
    @bp_app.route("/runs", methods=["GET"])
    @token_auth
    def get_runs():
        data = get_run_status_list()
        response = jsonify(data)
        response.status_code = 200
        return response


# python3 ./tests/post_runs_mock/post_runs_mock_trim.py
@bp_app.route("/runs", methods=["POST"])
@token_auth
def post_runs():
    parameters = validate_and_format_post_runs_request(request)
    data = execute(parameters)
    response = jsonify(data)
    response.status_code = 200
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
    response.status_code = 200
    return response
