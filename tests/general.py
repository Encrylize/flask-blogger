import unittest

from app import create_app, db


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

        # Temporary. Will be removed once default settings has been set up.
        self.app.config["SETTINGS"]['posts_per_page'] = '10'
        self.app.config["SETTINGS"]['blog_name'] = 'flask-blogger'

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()


class DummyPostData(dict):
    def getlist(self, key):
        v = self[key]
        if not isinstance(v, (list, tuple)):
            v = [v]
        return v
