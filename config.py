import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Base configuration with values used in all configurations. """

    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    DEFAULT_SETTINGS = [{
            'key': 'blog_name',
            'name': 'Blog name',
            'value': 'Flask-Blogger'
        },
        {
            'key': 'posts_per_page',
            'name': 'Posts per page',
            'value': 10
        },
        {
            'key': 'show_login_link',
            'name': 'Show login link',
            'value': True
        }
    ]


class DevelopmentConfig(Config):
    """
    Development configuration.
    Activates the debugger.

    """

    DEBUG = True
    WHOOSH_BASE = os.path.join(basedir, 'dev_search_database')
    CACHE_TYPE = 'simple'


class TestingConfig(Config):
    """
    Testing configuration.
    Sets the testing flag to True.

    """

    TESTING = True
    WTF_CSRF_ENABLED = False
    CACHE_TYPE = 'simple'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
