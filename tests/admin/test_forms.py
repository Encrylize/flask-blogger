from app.models import Tag
from app.admin.forms import PostForm
from tests.general import AppTestCase, DummyPostData


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
        form_3.tags.data = ['foo', 'bar', 'baz', 'duplicate', 'duplicate']
        form_3.save()

        tag_1 = Tag.query.filter_by(name='baz').first()
        tag_2 = Tag.query.filter_by(name='foo bar').first()

        self.assertIsNotNone(tag_1)
        self.assertNotIn(tag_2, post_1.tags.all())
        self.assertEqual(Tag.query.filter_by(name='duplicate').count(), 1)
