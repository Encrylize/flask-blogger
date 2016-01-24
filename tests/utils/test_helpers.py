from flask import url_for

from app import db
from app.models import Post
from app.utils.helpers import get_or_create, get_redirect_target, is_safe_url
from tests.general import AppTestCase


class TestHelpers(AppTestCase):
    def test_get_or_create(self):
        post_1, created_1 = get_or_create(Post, title='foo', short_text='bar')
        db.session.add(post_1)
        db.session.commit()
        post_2, created_2 = get_or_create(Post, title='foo', short_text='bar')

        self.assertTrue(created_1)
        self.assertFalse(created_2)
        self.assertEqual(post_1, post_2)

    def test_is_safe_url(self):
        with self.app.test_request_context():
            self.assertFalse(is_safe_url('http://externalsite.com'))
            self.assertTrue(is_safe_url(url_for('main.index', _external=True)))
            self.assertTrue(is_safe_url('safe_internal_link'))

    def test_get_redirect_target(self):
        with self.app.test_request_context('/?next=http://externalsite.com'):
            self.assertIsNone(get_redirect_target())

        with self.app.test_request_context('/?next=safe_internal_link'):
            self.assertEqual(get_redirect_target(), 'safe_internal_link')

