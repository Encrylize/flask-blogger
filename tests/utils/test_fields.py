from wtforms import Form

from app.models import Post, Tag
from app.utils.fields import TagListField
from tests.general import AppTestCase, DummyPostData


class TestFields(AppTestCase):
    class TestForm(Form):
        tag_list_field = TagListField()

    def test_tag_list_field(self):
        form = self.TestForm(DummyPostData(tag_list_field='foo, bar, foo bar,   whitespace    ,'))
        self.assertEquals(form.tag_list_field.data, ['foo', 'bar', 'foo bar', 'whitespace'])

        post = Post(title='foo', short_text='bar')
        tag_1 = Tag(name='foo')
        tag_2 = Tag(name='bar')
        post.tags.append(tag_1)
        post.tags.append(tag_2)
        post.save()
        form = self.TestForm(DummyPostData(tag_list_field=post.tags))
        self.assertEquals(form.tag_list_field.data, ['foo', 'bar'])
