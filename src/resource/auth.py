from flask_restx import Resource, reqparse

from model.app import App
from model.auth import AuthModel
import u_util

class AuthResource(Resource):
    """ Authentication API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = App.get_instance().config["CURRENT_KEY"]
        self.db = App.get_instance().config["CURRENT_DB"]

    def get(self):
        """ Health check """
        return {"code": 200, "msg": "auth service is up"}, 200

    def post(self):
        """ New user registration """
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("password")
        args = parser.parse_args()

        user = AuthModel.query.filter_by(username = args["username"]).first()
        if user is not None:
            resp = {"code": 400, "msg": "username is already existed"}
            return resp, 400

        user = AuthModel(args["username"], args["password"])
        self.db.session.add(user)
        self.db.session.commit()

        payload = {"id": user.id}
        token = u_util.encode_jwt_token(payload, self.key)
        resp = {"code": 200, "msg": "new user is created", "token": token}
        return resp, 200
