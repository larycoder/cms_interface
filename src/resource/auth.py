import json
from urllib.parse import quote

from flask import redirect, request
from flask_restx import Namespace, reqparse
import requests

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
        resp_with_cookie = self.build_resp(resp)
        resp_with_cookie.set_cookie("Authorization", "bearer " + token)
        return resp_with_cookie


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
            resp = ""
            msg = "wrong username or password"
            code = 403

        resp_with_cookie = self.build_resp(Response(code, msg, resp))
        resp_with_cookie.set_cookie("Authorization", "bearer " + resp)
        return resp_with_cookie


@ns.route("/blue-button")
class BlueButtonResource(BaseResource):
    """Request code from blue-button"""

    @u_util.check_auth
    def get(self):
        app = App.get_instance()
        bluebutton_auth_url = app.config["BLUEBUTTON_AUTH_URL"]

        req_param = {
            "response_type": "code",
            "client_id": quote(app.config["CLIENT_ID"]),
            "redirect_uri": quote(app.config["REDIRECT_URI"]),
        }
        req_param_str = "&".join([f"{k}={v}" for k, v in req_param.items()])

        req_str = f"{bluebutton_auth_url}/?{req_param_str}"
        return redirect(req_str)


@ns.route("/callback")
class BlueButtonCallbackResource(BaseResource):
    """Retrieve blue button access code"""

    def parse_bb_auth_content(self, resp):
        if resp.status_code != 200:
            return None
        else:
            return json.loads(resp.content.decode())

    @u_util.check_auth
    def get(self):
        payload = u_util.get_payload_from_req_tok()
        if payload is None:
            return self.build_resp(Response(401, "missing payload"))
        elif payload["code"] == 401:
            resp = Response(payload["code"], "error payload", str(payload["resp"]))
            return self.build_resp(resp)
        else:
            payload = payload["resp"]

        user = AuthModel.query.get(payload["id"])
        if user is None:
            return self.build_resp(Response(404, "undefined user"))

        bb_code = request.args.get("code")
        if bb_code is not None:
            tok_url = App.get_instance().config["BLUEBUTTON_TOKEN_URL"]
            tok_client_id = App.get_instance().config["CLIENT_ID"]
            tok_client_secret = App.get_instance().config["CLIENT_SECRET"]
            tok_callback = App.get_instance().config["REDIRECT_URI"]
            tok_data = {
                "grant_type": "authorization_code",
                "code": bb_code,
                "redirect_uri": tok_callback,
                "client_id": tok_client_id,
                "client_secret": tok_client_secret,
            }
            resp = requests.post(tok_url, tok_data)
            data = self.parse_bb_auth_content(resp)
            if data is None:
                return self.build_resp(
                    Response(resp.status_code, "", resp.content.decode())
                )
            else:
                user.bb_access_token = data["access_token"]
                user.bb_refresh_token = data["refresh_token"]
                self.db.session.commit()

                return self.build_resp(
                    Response(200, "successfully update blue button code", data)
                )
        else:
            return self.build_resp(Response(404, "callback fail"))
