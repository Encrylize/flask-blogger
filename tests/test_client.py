from flask import url_for

from app import db, user_datastore
from app.models import Post, Tag
from tests.general import AppTestCase


class ClientTestCase(AppTestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client(use_cookies=True)


class TestAdminBlueprint(ClientTestCase):
    def setUp(self):
        super().setUp()

        # Create user and log in
        user_datastore.create_user(email='foo@bar.com', password='foobar')
        self.client.post(url_for('security.login'), data={
            'email': 'foo@bar.com',
            'password': 'foobar'
        }, follow_redirects=True)

    def test_login_required(self):
        response = self.client.get(url_for('admin.index'))

        self.assertEqual(response._status, '200 OK')

        # Log out
        self.client.get(url_for('security.logout'))
        response = self.client.get(url_for('admin.index'))

        # Assert response code is a redirect
        self.assertEqual(response._status, '302 FOUND')

    def test_new_post(self):
        self.client.post(url_for('admin.new_post'), data={
            'title': 'foo',
            'short_text': 'bar',
            'long_text': 'baz',
            'tags': 'foobar'
        })
        post = Post.query.first()

        self.assertIsNotNone(post)

    def test_edit_post(self):
        post = Post(title='foo', short_text='bar', long_text='baz').save()

        self.client.post(url_for('admin.edit_post', id=post.id, slug=post.slug), data={
            'title': 'baz',
            'short_text': 'foo',
            'long_text': 'bar',
            'tags': 'foobar'
        })

        self.assertEqual(post.title, 'baz')
        self.assertEqual(post.short_text, 'foo')
        self.assertEqual(post.long_text, 'bar')
        self.assertIsNotNone(Tag.query.first())

        response = self.client.get(url_for('admin.edit_post', id=post.id))

        self.assertEqual(response.headers['Location'],
                         url_for('admin.edit_post', id=post.id, slug=post.slug, _external=True))

        response = self.client.post(url_for('admin.edit_post', id=post.id, slug=post.slug), data={
                     'title': 'baz',
                   }, follow_redirects=True)

        self.assertIn(b'Please fill out at least one of these fields.', response.data)

    def test_delete_post(self):
        post = Post(title='foo', short_text='bar')
        db.session.add(post)
        db.session.commit()

        response = self.client.get(url_for('admin.delete_post', id=post.id))

        # Assert response code is a redirect
        self.assertEqual(response._status, '302 FOUND')
        self.assertIsNone(Post.query.first())


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
