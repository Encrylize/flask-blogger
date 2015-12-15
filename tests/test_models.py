from datetime import datetime
import unittest

from freezegun import freeze_time

from app import create_app, db
from app.models import Post


class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    @freeze_time(datetime.now())
    def test_post_initialization(self):
        post = Post(title='foo', body='bar')
        db.session.add(post)
        db.session.commit()

        self.assertEqual(datetime.now(), post.timestamp)
        self.assertEqual(post.title, 'foo')
        self.assertEqual(post.body, 'bar')
