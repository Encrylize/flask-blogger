from flask import url_for
from wtforms import Form

from app import db
from app.models import Post, Tag
from app.admin.forms import PostForm
from app.utils.fields import TagListField
from app.utils.helpers import get_or_create, get_redirect_target, is_safe_url
from tests.general import AppTestCase, DummyPostData


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


class TestFields(AppTestCase):
    class TestForm(Form):
        tag_list_field = TagListField()

    def test_tag_list_field(self):
        post = Post(title='foo', short_text='bar')
        db.session.add(post)
        db.session.commit()

        tag_1, tag_2 = Tag(name='tag 1'), Tag(name='tag 2')
        post.tags.extend([tag_1, tag_2])

        form_1 = self.TestForm(DummyPostData(tag_list_field=post.tags))
        form_2 = self.TestForm(DummyPostData(tag_list_field='foo, bar, foo bar,   whitespace    ,'))

        self.assertEqual(form_1.tag_list_field.data, ['tag 1', 'tag 2'])
        self.assertEqual(form_2.tag_list_field.data, ['foo', 'bar', 'foo bar', 'whitespace'])



class TestPostForm(AppTestCase):
    def test_save(self):
        form_1 = PostForm(DummyPostData(title='foo', short_text='bar', tags='foo, bar, foo bar'))
        post_1 = form_1.save()
        tags_1 = Tag.query.all()

        self.assertListEqual(tags_1, post_1.tags.all())

        form_2 = PostForm(DummyPostData(title='foo', short_text='bar', tags='foo, bar, someothertag'))
        form_2.save()
        
        self.assertEqual(len(Tag.query.all()), 4)

        form_3 = PostForm(obj=post_1)
        form_3.tags.data = ['foo', 'bar', 'baz']
        form_3.save()

        tag1 = Tag.query.filter_by(name='baz').first()
        tag2 = Tag.query.filter_by(name='foo bar').first()

        self.assertIsNotNone(tag1)
        self.assertNotIn(tag2, post_1.tags.all())
