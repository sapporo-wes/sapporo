# coding: utf-8
from flask import Blueprint, jsonify

from .lib.service import read_service_setting_file
from .lib.workflows import read_workflow_setting_file

bp_app = Blueprint("app", __name__)


@bp_app.route("/service-info", methods=["GET"])
def service_info():
    data = read_service_setting_file()
    response = jsonify(data)
    response.status_code = 200
    return response


@bp_app.route("/workflows", methods=["GET"])
def workflows_list():
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
def workflows_list():
    data = read_workflow_setting_file()
    response = jsonify(data)
    response.status_code = 200
    return response
