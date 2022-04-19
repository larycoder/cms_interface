# Register resource to endpoint

from flask import Blueprint
from flask_restx import Api


def load_blueprint():
    from resource.auth import AuthResource

    bp = Blueprint("api", __name__)
    api = Api(bp, prefix="/api")
    api.add_resource(AuthResource, "/auth")
    return bp
