import unittest

from app import create_app, configure_settings, db


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()
        configure_settings(self.app)

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
