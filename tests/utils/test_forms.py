from wtforms.fields import StringField

from app.utils.forms import RedirectForm
from tests import AppTestCase


class TestRedirectForm(AppTestCase):
    class TestForm(RedirectForm):
        foo = StringField()
        bar = StringField()

    def test_populate_obj(self):
        # Simulates an object, where one can use setattr(obj, attr, value) to set an attribute
        obj = lambda: None
        form = self.TestForm(foo='bar', bar='foo')
        form.populate_obj(obj)

        self.assertEqual(obj.foo, 'bar')
        self.assertEqual(obj.bar, 'foo')
        with self.assertRaises(AttributeError):
            obj.next
