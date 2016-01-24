from flask import url_for

from app.models import Post, Tag
from tests.general import ClientTestCase


class TestMainBlueprint(ClientTestCase):
    def test_show_post(self):
        post = Post(title='foo', short_text='bar', long_text='baz').save()
        response = self.client.get(url_for('main.show_post', id=post.id), follow_redirects=True)

        self.assertIn(b'foo', response.data)
        self.assertIn(b'bar', response.data)
        self.assertIn(b'baz', response.data)

    def test_show_tag(self):
        post = Post(title='foo', short_text='bar', long_text='baz').save()
        tag = Tag(name='qux')
        post.tags.append(tag)

        response = self.client.get(url_for('main.show_tag', id=1), follow_redirects=True)

        self.assertIn(b'foo', response.data)
        self.assertIn(b'bar', response.data)
