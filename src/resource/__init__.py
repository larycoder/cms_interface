from flask import request
from flask_restx import Resource
from model.app import App
from model.response import Response
import u_util


class BaseResource(Resource):
    """Abstract class for resource"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = App.get_instance().config["CURRENT_KEY"]
        self.db = App.get_instance().config["CURRENT_DB"]

    def build_resp(self, resp: Response):
        return (resp.to_dict(), resp.code)

    def is_valid_token(self):
        def not_auth():
            resp = Response(401, "Unauthorized")
            return (resp.to_dict(), resp.code)

        if request is None:
            return not_auth()
        else:
            auth = request.headers.get("Authorization")
            if not auth:
                return not_auth()
            elif not isinstance(auth, str):
                return not_auth()
            elif not auth.lower().startswith("bearer"):
                return not_auth()
            else:
                token = auth.split()[1]
                key = App.get_instance().config["CURRENT_KEY"]
                sub = u_util.decode_jwt_token(token, key)
                print(sub)
                if sub["code"] == 401:
                    return not_auth()
                else:
                    return None
