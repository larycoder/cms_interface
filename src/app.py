import json

from flask_sqlalchemy import SQLAlchemy

from model.app import App
from route import load_blueprint
import u_util


def init_app():
    """
    Initialize app
    """
    #config_path = input("configuration path [ ../config.json ]: ")
    config_path = ""
    if len(config_path) == 0:
        config_path = "../config.json"

    with open(config_path, "r") as f:
        config = json.loads(f.read())

    print("Initializing app and postgres connection...", end=" ")
    app = App.get_instance()
    app.config.update(**config)
    app.config["CURRENT_DB"] = SQLAlchemy(app)
    app.config["CURRENT_KEY"] = u_util.b64_to_byte(app.config["SECRET_KEY"])
    app.register_blueprint(load_blueprint())
    print("Done")
    return app


def migrate(db):
    """
    Migrate model to database
    """
    from model.auth import AuthModel

    u_util.execute(
        db.engine.execute, "Test database connection...", "SELECT 1")

    u_util.execute(
        db.create_all, "Migrating data to database...")

# Driver
if __name__ == "__main__":
    app = init_app()
    if app.config["USER_MIGRATION"] is True:
        migrate(app.config["CURRENT_DB"])
    else:
        app.run("0.0.0.0", 5000, debug=True)
