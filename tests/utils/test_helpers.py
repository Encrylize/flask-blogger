import unittest

from app import create_app, db
from app.models import Post
from app.utils.helpers import get_or_create


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def test_get_or_create(self):
        post1, created1 = get_or_create(Post, title='foo', body='bar')
        db.session.add(post1)
        db.session.commit()
        post2, created2 = get_or_create(Post, title='foo', body='bar')
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEquals(post1, post2)
