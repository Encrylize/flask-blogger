import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Base configuration with values used in all configurations. """

    SERVER_NAME = os.getenv('SERVER_NAME', 'localhost:5000')
    SECRET_KEY = os.getenv('SECRET_KEY')
    BLOG_NAME = os.getenv('BLOG_NAME', 'Unnamed Blog')

    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    """
    Development configuration.
    Activates the debugger and uses the database specified
    in the DEV_DATABASE_URL environment variable.

    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')


class TestingConfig(Config):
    """
    Testing configuration.
    Sets the testing flag to True and uses the database
    specified in the TEST_DATABASE_URL environment variable.

    """

    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
