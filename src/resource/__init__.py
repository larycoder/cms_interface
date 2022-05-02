from flask_restx import Resource
from model.app import App
from model.response import Response


class BaseResource(Resource):
    """ Abstract class for resource """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = App.get_instance().config["CURRENT_KEY"]
        self.db = App.get_instance().config["CURRENT_DB"]

    def build_resp(self, resp: Response):
        return (resp.to_dict(), resp.code)
