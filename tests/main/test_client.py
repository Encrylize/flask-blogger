from flask import url_for

from app import db
from app.admin.models import User
from app.main.models import Post, Tag
from tests import ClientTestCase


class TestMainBlueprint(ClientTestCase):
    def test_show_post(self):
        user = User(email='foo@bar.com', name='Foo Bar', slug='foobar', password='foobar')
        post = Post(title='foo', short_text='bar', long_text='baz', slug='foo', author=user)
        db.session.add_all([user, post])
        db.session.commit()

        response = self.client.get(url_for('main.show_post', id=post.id), follow_redirects=True)

        self.assertIn(b'Foo Bar', response.data)
        self.assertIn(b'foo', response.data)
        self.assertIn(b'bar', response.data)
        self.assertIn(b'baz', response.data)

    def test_show_tag(self):
        user = User(email='foo@bar.com', name='Foo Bar', slug='foobar', password='foobar')
        post = Post(title='foo', short_text='bar', long_text='baz', slug='foo', author=user)
        db.session.add_all([user, post])
        db.session.commit()

        tag = Tag(name='qux')
        post.tags.append(tag)

        response = self.client.get(url_for('main.show_tag', id=1), follow_redirects=True)

        self.assertIn(b'foo', response.data)
        self.assertIn(b'bar', response.data)
