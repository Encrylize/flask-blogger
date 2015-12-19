import unittest

from app import create_app, db
from app.utils.forms import RedirectForm


class TestRedirectForm(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.redirect_form = RedirectForm()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def test_is_safe_url(self):
        with self.app.test_request_context():
            self.assertFalse(self.redirect_form.is_safe_url('http://externalsite.com'))
            self.assertTrue(self.redirect_form.is_safe_url('http://' + self.app.config[
                'SERVER_NAME']))
            self.assertTrue(self.redirect_form.is_safe_url('safe_internal_link'))

    def test_get_redirect_target(self):
        with self.app.test_request_context('/?next=http://externalsite.com'):
            self.assertIsNone(self.redirect_form.get_redirect_target())

        with self.app.test_request_context('/?next=safe_internal_link'):
            self.assertEquals(self.redirect_form.get_redirect_target(), 'safe_internal_link')
