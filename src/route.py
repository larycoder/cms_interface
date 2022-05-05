from flask import Blueprint
from flask_restx import Api


def load_blueprint():
    from resource.auth import ns as auth

    bp = Blueprint("api", __name__)
    api = Api(bp, prefix="/api")

    api.add_namespace(auth)

    return bp
