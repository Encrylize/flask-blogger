from app.models import Post, Tag
from app.admin.forms import PostForm
from tests.general import AppTestCase, DummyPostData


class TestPostForm(AppTestCase):
    def setUp(self):
        super().setUp()
        self.form = PostForm

    def test_save(self):
        form = self.form(DummyPostData(title='foo', body='bar', tags='foo, bar, foo bar'))
        form.save()

        post1 = Post.query.first()
        tags = Tag.query.all()
        self.assertEquals(tags, post1.tags.all())

        form = self.form(DummyPostData(title='foo', body='bar', tags='foo, bar, someothertag'))
        form.save()

        post2 = Post.query.all()[-1]
        tag = Tag.query.filter_by(name='someothertag').first()
        self.assertIn(tag, post2.tags.all())
        self.assertNotIn(tag, post1.tags.all())

        form = self.form(obj=post1)
        form.tags.data = ['foo', 'bar', 'baz']
        form.save()

        post1 = Post.query.first()
        tag1 = Tag.query.filter_by(name='baz').first()
        tag2 = Tag.query.filter_by(name='foo bar').first()
        self.assertIsNotNone(tag1)
        self.assertNotIn(tag2, post1.tags.all())
