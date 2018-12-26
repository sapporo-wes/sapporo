from flask import Blueprint


bp_app = Blueprint("app", __name__)


@bp_app.route("/")
def index():
    return "Blue Print App"
