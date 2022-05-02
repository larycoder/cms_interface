# Register resource to endpoint

from flask import Blueprint
from flask_restx import Api


def load_blueprint():
    from resource.auth import LoginResource
    from resource.auth import RegisterResource

    bp = Blueprint("api", __name__)
    api = Api(bp, prefix="/auth")

    api.add_resource(RegisterResource, "/register")
    api.add_resource(LoginResource, "/login")

    return bp
