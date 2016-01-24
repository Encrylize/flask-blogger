import unittest

from app import create_app, db, populate_settings


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

        # Now that the Setting table has been created, we can populate the settings.
        populate_settings(self.app)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()


class ClientTestCase(AppTestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client(use_cookies=True)


class DummyPostData(dict):
    def getlist(self, key):
        v = self[key]
        if not isinstance(v, (list, tuple)):
            v = [v]
        return v
