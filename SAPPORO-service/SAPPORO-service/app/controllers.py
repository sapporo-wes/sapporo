# coding: utf-8
from flask import Blueprint, jsonify, request, abort

from .lib.service import read_service_setting_file
from .lib.workflows import read_workflow_setting_file
from .lib.runs import execute_run

bp_app = Blueprint("app", __name__)


@bp_app.route("/service-info", methods=["GET"])
def get_service_info():
    data = read_service_setting_file()
    response = jsonify(data)
    response.status_code = 200
    return response


@bp_app.route("/workflows", methods=["GET"])
def get_workflows_list():
    data = read_workflow_setting_file()
    response = jsonify(data)
    response.status_code = 200
    return response


# @bp_app.route("/runs", methods=["GET"])
# def workflows_list():
#     data = read_workflow_setting_file()
#     response = jsonify(data)
#     response.status_code = 200
#     return response


@bp_app.route("/runs", methods=["POST"])
def post_runs():
    fields = [field for field in request.form]
    values = [request.form[field] for field in request.form]
    data = dict(zip(fields, values))
    uuid = execute_run(data)
    if uuid is None:
        abort(404)
    response = jsonify({"run_id": uuid})
    response.status_code = 200
    return response
