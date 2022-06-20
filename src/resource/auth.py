from urllib.parse import quote

from flask import redirect
from flask_restx import Namespace, reqparse

from model.app import App
from model.auth import AuthModel
from model.response import Response
import u_util

from . import BaseResource

ns = Namespace(name="auth")


@ns.route("/health")
class HealthResource(BaseResource):
    """Validate token base request"""

    @u_util.check_auth
    def get(self):
        resp = Response(200, "Token is good")
        return self.build_resp(resp)


@ns.route("/register")
class RegisterResource(BaseResource):
    """Registration API"""

    post_parser = reqparse.RequestParser()
    post_parser.add_argument("username", type=str, location="json")
    post_parser.add_argument("password", type=str, location="json")

    @ns.expect(post_parser)
    def post(self):
        """New user registration"""
        args = RegisterResource.post_parser.parse_args()
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


@ns.route("/login")
class LoginResource(BaseResource):
    """Login API"""

    post_parser = reqparse.RequestParser()
    post_parser.add_argument("username", location="json")
    post_parser.add_argument("password", location="json")

    @ns.expect(post_parser)
    def post(self):
        """Login user"""
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


@ns.route("/blue-button")
class BlueButtonResource(BaseResource):
    """Request token from blue-button"""

    #@u_util.check_auth
    def get(self):
        app = App.get_instance()
        bluebutton_auth_url = app.config["BLUEBUTTON_AUTH_URL"]

        req_param = {
            "response_type": "code",
            "client_id": quote(app.config["CLIENT_ID"]),
            "redirect_uri": quote(app.config["REDIRECT_URI"])
        }
        req_param_str = "&".join([f"{k}={v}" for k, v in req_param.items()]);

        req_str = f"{bluebutton_auth_url}/?{req_param_str}"
        return redirect(req_str)
