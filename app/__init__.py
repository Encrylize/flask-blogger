from flask import Flask
from flask_cache import Cache
from flask_login import LoginManager
from flask_misaka import Misaka
from flask_moment import Moment
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_whooshalchemy import whoosh_index
from sqlalchemy.exc import ProgrammingError

from config import config

cache = Cache()
db = SQLAlchemy()
lm = LoginManager()
markdown = Misaka()
moment = Moment()
security = Security()

from app.main.models import Post
from app.admin.models import User, Role, Setting
from app.utils.settings import AppSettings

from app.main import main
from app.admin import admin

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app(config_name):
    """
    Initializes a Flask app.

    Args:
        config_name: The configuration class to use.

    Returns:
        The Flask app object.

    """

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    configure_extensions(app)
    configure_settings(app)
    configure_blueprints(app)

    return app


def configure_settings(app):
    """
    Configures the AppSettings interface for an app.

    Args:
        app: The Flask app object to attach the interface to.

    """

    with app.app_context():
        app.config['SETTINGS'] = AppSettings()
        try:
            populate_settings(app)
        except ProgrammingError:
            # Settings table does not exist.
            # Catch the error, so Flask-Migrate can still function.
            pass

    @app.context_processor
    def inject_settings():
        return dict(settings=app.config['SETTINGS'])


def configure_extensions(app):
    """
    Configures the Flask extensions for an app.

    Args:
        app: The Flask app object to initialize the extensions with.

    """

    db.init_app(app)
    lm.init_app(app)
    cache.init_app(app, app.config)
    markdown.init_app(app)
    moment.init_app(app)
    security.init_app(app, user_datastore)
    whoosh_index(app, Post)

    app.jinja_env.add_extension('jinja2.ext.do')


def configure_blueprints(app):
    """
    Configures the blueprints for an app.

    Args:
        app: The Flask app object to register the blueprints on.

    """

    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')


def populate_settings(app):
    """
    Populates the settings with defaults from the app config.
    Settings that are already set will not be overridden.

    Args:
        app: The Flask app object.

    """

    for setting in app.config['DEFAULT_SETTINGS']:
        if setting['key'] not in app.config['SETTINGS'].keys():
            setting = Setting(**setting)
            setting.save()
    app.config['SETTINGS']['installed'] = True
