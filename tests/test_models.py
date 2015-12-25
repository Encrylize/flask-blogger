from datetime import datetime

from freezegun import freeze_time
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Post, Tag
from tests.general import AppTestCase


class TestPost(AppTestCase):
    @freeze_time(datetime.now())
    def test_initialization(self):
        post = Post(title='title ', short_text='short text', long_text='long text').save()

        self.assertEqual(datetime.now(), post.timestamp)

    def test_tags_relationship(self):
        post_1 = Post(title='post 1', short_text='short text')
        post_2 = Post(title='post 2', short_text='short text')
        db.session.add_all([post_1, post_2])
        db.session.commit()

        tag_1, tag_2 = Tag(name='tag 1'), Tag(name='tag 2')
        post_1.tags.extend([tag_1, tag_2])
        post_2.tags.append(tag_1)

        self.assertIn(tag_1, post_1.tags.all())
        self.assertIn(tag_2, post_1.tags.all())
        self.assertIn(post_1, tag_1.posts.all())
        self.assertIn(post_2, tag_1.posts.all())
        self.assertNotIn(post_2, tag_2.posts.all())

    def test_save(self):
        post_1 = Post(title='Hello World! ß', short_text='foobar').save()

        self.assertIsNotNone(Post.query.first())
        self.assertEqual(post_1.slug, 'hello-world-ss')

    def test_short_text_or_long_text_is_not_null(self):
        post_1 = Post(title='post 1')

        self.assertRaises(IntegrityError, post_1.save)


class TestTag(AppTestCase):
    def test_auto_delete_orphan(self):
        post = Post(title='foo', short_text='bar', long_text='baz')
        db.session.add(post)
        db.session.commit()

        tag = Tag(name='foobar')
        post.tags.append(tag)

        self.assertIsNotNone(Tag.query.first())

        post.tags.remove(tag)

        self.assertIsNone(Tag.query.first())

        tag = Tag(name='foobar')
        post.tags.append(tag)
        db.session.delete(post)
        db.session.commit()

        self.assertIsNone(Tag.query.first())

    def test_add_slug_before_insert(self):
        post = Post(title='foo', short_text='bar', long_text='baz')
        db.session.add(post)
        db.session.commit()

        tag = Tag(name='foo bar')
        post.tags.append(tag)
        tag = Tag.query.first()

        self.assertEqual(tag.slug, 'foo-bar')
