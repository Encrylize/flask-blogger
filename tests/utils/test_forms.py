import unittest

from app import create_app, db
from app.utils.forms import RedirectForm


class FormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()


class TestRedirectForm(FormTestCase):
    def setUp(self):
        super().setUp()
        self.form = RedirectForm()

    def test_is_safe_url(self):
        with self.app.test_request_context():
            self.assertFalse(self.form.is_safe_url('http://externalsite.com'))
            self.assertTrue(self.form.is_safe_url('http://' + self.app.config[
                'SERVER_NAME']))
            self.assertTrue(self.form.is_safe_url('safe_internal_link'))

    def test_get_redirect_target(self):
        with self.app.test_request_context('/?next=http://externalsite.com'):
            self.assertIsNone(self.form.get_redirect_target())

        with self.app.test_request_context('/?next=safe_internal_link'):
            self.assertEquals(self.form.get_redirect_target(), 'safe_internal_link')
