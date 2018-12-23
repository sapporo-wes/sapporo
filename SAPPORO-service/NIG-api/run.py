# coding: utf-8
from flask import Flask, jsonify
from dummy_data import DUMMY_SERVICE_INFO, DUMMY_RUNS_LIST, DUMMY_RUNS_RUN, DUMMY_RUNS_INFO, DUMMY_RUNS_CANCEL, DUMMY_RUNS_STATUS


app = Flask(__name__)


@app.route("/service-info", methods=["GET"])
def service_info():
    response = jsonify(DUMMY_SERVICE_INFO)
    response.status_code = 200
    return response


@app.route("/runs", methods=["GET"])
def runs_list():
    response = jsonify(DUMMY_RUNS_LIST)
    response.status_code = 200
    return response


@app.route("/runs", methods=["POST"])
def runs_run():
    response = jsonify(DUMMY_RUNS_RUN)
    response.status_code = 200
    return response


@app.route("/runs/<int:run_id>", methods=["GET"])
def runs_info(run_id):
    response = jsonify(DUMMY_RUNS_INFO)
    response.status_code = 200
    return response


@app.route("/runs/<int:run_id>/cancel", methods=["POST"])
def runs_cancel(run_id):
    response = jsonify(DUMMY_RUNS_CANCEL)
    response.status_code = 200
    return response


@app.route("/runs/<int:run_id>/status", methods=["GET"])
def runs_status(run_id):
    response = jsonify(DUMMY_RUNS_STATUS)
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
