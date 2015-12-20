from datetime import datetime

from freezegun import freeze_time

from app import db
from app.models import Post, Tag
from tests.general import AppTestCase


class TestModels(AppTestCase):
    @freeze_time(datetime.now())
    def test_post_initialization(self):
        post = Post(title='foo', body='bar')
        db.session.add(post)
        db.session.commit()

        self.assertEqual(datetime.now(), post.timestamp)
        self.assertEqual(post.title, 'foo')
        self.assertEqual(post.body, 'bar')

    def test_posts_tags_relationship(self):
        post_1 = Post(title='foo', body='bar')
        post_2 = Post(title='foo', body='bar')
        tag_1 = Tag(name='tag 1')
        tag_2 = Tag(name='tag 2')
        post_1.tags.append(tag_1)
        post_1.tags.append(tag_2)
        post_2.tags.append(tag_1)
        db.session.add_all([post_1, post_2, tag_1, tag_2])
        db.session.commit()

        self.assertIn(tag_1, post_1.tags)
        self.assertIn(tag_2, post_1.tags)
        self.assertNotIn(tag_2, post_2.tags)
        self.assertIn(post_1, tag_1.posts)
        self.assertIn(post_2, tag_1.posts)
        self.assertNotIn(post_2, tag_2.posts)

    def test_post_save(self):
        post_1 = Post(title=u'Hello World! ß', body='foobar')
        post_1.save()

        post_2 = Post(title=u'Hello World! ß', body='foobar')
        post_2.save()

        self.assertEquals(post_1.slug, 'hello-world-ss')
        self.assertEquals(post_2.slug, 'hello-world-ss2')
