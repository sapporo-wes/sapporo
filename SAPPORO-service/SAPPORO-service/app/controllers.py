# coding: utf-8
from flask import Blueprint, jsonify

from .lib.service_info import read_setting_file

bp_app = Blueprint("app", __name__)


@bp_app.route("/service-info", methods=["GET"])
def service_info():
    data = read_setting_file()
    response = jsonify(data)
    response.status_code = 200
    return response
