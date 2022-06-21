from model.app import App

db = App.get_instance().config["CURRENT_DB"]


class AuthModel(db.Model):
    """Model for authentication"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    bb_access_token = db.Column(db.String(255))
    bb_refresh_token = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password
