from app import db
from app.models import Post
from app.utils.helpers import get_or_create
from tests.general import AppTestCase


class TestUtils(AppTestCase):
    def test_get_or_create(self):
        post1, created1 = get_or_create(Post, title='foo', body='bar')
        db.session.add(post1)
        db.session.commit()
        post2, created2 = get_or_create(Post, title='foo', body='bar')
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEquals(post1, post2)
