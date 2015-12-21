from app.models import Post
from app.utils.helpers import get_or_create
from tests.general import AppTestCase


class TestHelpers(AppTestCase):
    def test_get_or_create(self):
        post1, created1 = get_or_create(Post, title='foo', body='bar')
        post1.save()
        post2, created2 = get_or_create(Post, title='foo', body='bar')
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEquals(post1, post2)
