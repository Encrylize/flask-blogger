from flask import url_for

from app import db, user_datastore
from app.main.models import Post, Tag
from tests import ClientTestCase


class TestAdminBlueprint(ClientTestCase):
    def setUp(self):
        super().setUp()

        # Create user
        user_datastore.create_user(email='foo@bar.com', password='foobar', name='Foo Bar')
        # Log in with the user we just created
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
        # Create a new post
        self.client.post(url_for('admin.new_post'), data={
            'title': 'foo',
            'short_text': 'bar',
            'long_text': 'baz',
            'tags': 'foobar'
        })
        post = Post.query.first()

        self.assertIsNotNone(post)

    def test_edit_post(self):
        post = Post(title='foo', short_text='bar', long_text='baz', slug='foo')
        db.session.add(post)
        db.session.commit()

        # Edit the post we just created
        self.client.post(url_for('admin.edit_post', id=post.id, slug=post.slug), data={
            'title': 'baz',
            'short_text': 'foo',
            'long_text': 'bar',
            'tags': 'foobar'
        })

        # Assert that the changes took place and a tag was added
        self.assertEqual(post.title, 'baz')
        self.assertEqual(post.short_text, 'foo')
        self.assertEqual(post.long_text, 'bar')
        self.assertIsNotNone(Tag.query.first())

        response = self.client.post(url_for('admin.edit_post', id=post.id, slug=post.slug), data={
                       'title': 'baz',
                   }, follow_redirects=True)

        # Assert that an error was raised, as a result of leaving both short_text and long_text empty
        self.assertIn(b'Please fill out at least one of these fields.', response.data)

    def test_delete_post(self):
        post = Post(title='foo', short_text='bar')
        db.session.add(post)
        db.session.commit()

        response = self.client.get(url_for('admin.delete_post', id=post.id))

        # Assert response code is a redirect
        self.assertEqual(response._status, '302 FOUND')
        self.assertIsNone(Post.query.first())

    def test_post_preview(self):
        response = self.client.post(url_for('admin.preview_post'), data={
                       'title': 'foo',
                       'short_text': 'bar',
                       'long_text': 'baz',
                       'tags': 'a, b, c'
                   })

        # Assert that the data are shown
        self.assertIn(b'foo', response.data)
        self.assertIn(b'bar', response.data)
        self.assertIn(b'baz', response.data)
        self.assertIn(b'a', response.data)
        self.assertIn(b'b', response.data)
        self.assertIn(b'c', response.data)

        response = self.client.get(url_for('admin.new_post'))

        # Assert that the data persisted on page change
        self.assertIn(b'foo', response.data)
        self.assertIn(b'bar', response.data)
        self.assertIn(b'baz', response.data)
        self.assertIn(b'a, b, c', response.data)

        with self.client.session_transaction() as session:
            # Assert that the post_preview data was deleted
            self.assertIsNone(session.get('post_preview'))

    def test_edit_settings(self):
        form_data = dict(self.app.config['SETTINGS'])
        form_data['blog_name'] = 'foobar'
        self.client.post(url_for('admin.edit_settings'), data=form_data)

        self.assertEqual(self.app.config['SETTINGS']['blog_name'], 'foobar')
