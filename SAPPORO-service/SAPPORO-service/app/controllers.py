# coding: utf-8
from flask import Blueprint, current_app, jsonify, request

from .lib.runs import cancel_run, execute, get_run_info, get_run_status_list
from .lib.util import read_service_info
from .lib.workflows import read_workflow_setting_file
from .config import d_config

bp_app = Blueprint("app", __name__)

if d_config["DEBUG"] is False:
    @bp_app.errorhandler(400)
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


# python3 ./tests/post_runs_mock/post_runs_mock_trim.py
@bp_app.route("/runs", methods=["POST"])
def post_runs():
    parameters = dict(request.form)
    parameters["run_order"] = request.files["run_order"]
    data = execute(parameters)
    response = jsonify(data)
    response.status_code = 200
    return response


# curl -X GET localhost:8002/runs/317c8109-e259-4b31-9bfd-581a3170ae7a
@bp_app.route("/runs/<uuid:run_id>", methods=["GET"])
def get_runs_uuid(run_id):
    data = get_run_info(run_id)
    response = jsonify(data)
    response.status_code = 200
    return response


# curl -X POST localhost:8002/runs/317c8109-e259-4b31-9bfd-581a3170ae7a/cancel
@bp_app.route("/runs/<uuid:run_id>/cancel", methods=["POST"])
def post_runs_cancel(run_id):
    data = cancel_run(run_id)
    response = jsonify(data)
    response.status_code = 200
    return response
