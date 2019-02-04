# coding: utf-8
from flask import Flask
from .controllers import bp_app
from .config import d_config


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(d_config)
    app.register_blueprint(bp_app, url_prefix="/")

    return app
