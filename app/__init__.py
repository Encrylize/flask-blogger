from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
lm = LoginManager()
moment = Moment()
pagedown = PageDown()
security = Security()

from app.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app(config_name):
    """
    Initializes a Flask app.

    Args:
        config_name: The configuration object to use.

    Returns:
        The Flask app object.

    """

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    lm.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    security.init_app(app, user_datastore)

    from app.main.views import main
    from app.admin.views import admin
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')

    return app
