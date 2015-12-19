import unittest

from wtforms import Form

from app.utils.fields import TagListField


class DummyPostData(dict):
    def getlist(self, key):
        v = self[key]
        if not isinstance(v, (list, tuple)):
            v = [v]
        return v


class TestFields(unittest.TestCase):
    class TestForm(Form):
        tag_list_field = TagListField()

    def test_tag_list_field(self):
        form = self.TestForm(DummyPostData(tag_list_field='foo, bar, foo bar,   whitespace    ,'))
        self.assertEquals(form.tag_list_field.data, ['foo', 'bar', 'foo bar', 'whitespace'])
