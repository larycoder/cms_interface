from flask import Blueprint
from flask_restx import Api


def load_blueprint():
    from resource.auth import ns as auth

    bp = Blueprint("api", __name__)
    auth_doc = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}
    api = Api(bp, prefix="/api", authorizations=auth_doc, security="Bearer")

    api.add_namespace(auth)

    return bp
