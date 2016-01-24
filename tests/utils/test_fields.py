from wtforms import Form

from app import db
from app.models import Post, Tag
from app.utils.fields import TagListField
from tests.general import AppTestCase, DummyPostData


class TestTagListField(AppTestCase):
    class TestForm(Form):
        tag_list_field = TagListField()

    def test_field_data(self):
        post = Post(title='foo', short_text='bar')
        db.session.add(post)
        db.session.commit()

        tag_1 = Tag(name='tag 1')
        tag_2 = Tag(name='tag 2')
        post.tags.extend([tag_1, tag_2])

        form_1 = self.TestForm(DummyPostData(tag_list_field=post.tags))
        form_2 = self.TestForm(DummyPostData(tag_list_field='foo, bar, foo bar,   whitespace    ,'))

        self.assertEqual(form_1.tag_list_field.data, ['tag 1', 'tag 2'])
        self.assertEqual(form_2.tag_list_field.data, ['foo', 'bar', 'foo bar', 'whitespace'])
