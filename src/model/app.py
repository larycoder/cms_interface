from flask import Flask


class App:
    """Singleton application of program"""

    _instance = None

    @staticmethod
    def get_instance() -> Flask:
        if App._instance is None:
            App._instance = Flask(__name__)
        return App._instance
