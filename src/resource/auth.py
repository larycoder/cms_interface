from flask_restx import reqparse
from . import BaseResource
from model.auth import AuthModel
from model.response import Response
import u_util


class RegisterResource(BaseResource):
    """ Registration API """

    def post(self):
        """ New user registration """
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("password")
        args = parser.parse_args()

        user = AuthModel.query.filter_by(username=args["username"]).first()
        if user is not None:
            return self.build_resp(Response(400, "username is already existed"))

        username = args["username"]
        password = u_util.hash_pwd(args["password"])

        user = AuthModel(username, password)
        self.db.session.add(user)
        self.db.session.commit()

        payload = {"id": user.id}
        token = u_util.encode_jwt_token(payload, self.key)
        resp = Response(200, "new user is created", token)
        return self.build_resp(resp)


class LoginResource(BaseResource):
    """ Login API """

    def post(self):
        """ Login user """
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("password")
        args = parser.parse_args()

        user = AuthModel.query.filter_by(username=args["username"]).first()
        status = u_util.is_correct_pwd(args["password"], user.password)

        if status is True:
            payload = {"id": user.id}
            resp = u_util.encode_jwt_token(payload, self.key)
            msg = "login successfully"
            code = 200
        else:
            resp = None
            msg = "wrong username or password"
            code = 403

        return self.build_resp(Response(code, msg, resp))
