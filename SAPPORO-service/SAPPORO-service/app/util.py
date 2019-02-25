# coding: utf-8
import logging
from logging.config import dictConfig
from secrets import compare_digest

from flask import abort, jsonify, request

from .config import ENABLE_TOKEN_AUTH, LOG_LEVEL, d_config
from .lib.util import SERVICE_BASE_DIR
from .logging_config import local_dev, local_prod, wsgi_dev, wsgi_prod

root_logger = logging.getLogger()


def fix_errorhandler(app):
    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def error_handler(error):
        response = {
            "msg": error.description,
            "status_code": error.code,
        }
        response = jsonify(response)
        response.status_code = error.code
        return response

    @app.errorhandler(Exception)
    def error_handler_exception(exception):
        import traceback
        root_logger.error(exception.args[0])
        root_logger.debug(traceback.format_exc())
        response = {
            "msg": "The server encountered an internal error and was unable to complete your request.",
            "status_code": 500,
        }
        response = jsonify(response)
        response.status_code = 500
        return response

    return app


def token_auth(func):
    def wrapper(*args, **kwargs):
        if ENABLE_TOKEN_AUTH:
            token_list = SERVICE_BASE_DIR.joinpath(
                "config").joinpath("token_list.txt")
            if token_list.exists() is False:
                abort(401, "Unauthorized.")
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


def set_logger():
    if d_config["DEBUG"]:
        print(LOG_LEVEL)
        if LOG_LEVEL == "DEVELOPMENT":
            dictConfig(local_dev)
        else:
            dictConfig(local_prod)
    else:
        if LOG_LEVEL == "DEVELOPMENT":
            dictConfig(wsgi_dev)
        else:
            dictConfig(wsgi_prod)
