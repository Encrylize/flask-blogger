from flask import Flask
from flask_cache import Cache
from flask_login import LoginManager
from flask_misaka import Misaka
from flask_moment import Moment
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_whooshalchemy import whoosh_index

from config import config

cache = Cache()
db = SQLAlchemy()
lm = LoginManager()
markdown = Misaka()
moment = Moment()
security = Security()

from app.models import Post, User, Role
from app.utils.settings import AppSettings
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
    cache.init_app(app, app.config)
    markdown.init_app(app)
    moment.init_app(app)
    security.init_app(app, user_datastore)
    whoosh_index(app, Post)

    if not app.config['TESTING']:
        configure_settings(app)

    from app.main.views import main
    from app.admin.views import admin
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')

    return app


def configure_settings(app):
    """
    Configures the settings for an app.

    Args:
        app: The Flask app object to attach the settings to.

    """

    with app.app_context():
        app.config['SETTINGS'] = AppSettings()

    @app.context_processor
    def inject_settings():
        return dict(settings=app.config['SETTINGS'])

