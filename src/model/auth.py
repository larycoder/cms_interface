from model.app import App

db = App.get_instance().config["CURRENT_DB"]


class AuthModel(db.Model):
    """Model for authentication"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    bb_code = db.Column(db.String(255))

    def __init__(self, username, password, bb_code=None):
        self.username = username
        self.password = password
        self.bb_code = bb_code
