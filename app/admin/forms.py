from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired

from app.models import Post, Tag
from app.utils.helpers import get_or_create
from app.utils.forms import RedirectForm
from app.utils.fields import TagListField


class PostForm(RedirectForm):
    title = StringField('Title', [DataRequired()])
    short_text = TextAreaField('Short text (displayed as preview)')
    long_text = TextAreaField('Long text')
    tags = TagListField('Tags (separated by comma)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = kwargs.get('obj')

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        if not self.short_text.data and not self.long_text.data:
            self.short_text.errors.append('Please fill out at least one of these fields.')
            self.long_text.errors.append('Please fill out at least one of these fields.')
            return False

        return True

    def save(self):
        """
        Saves the Post object.

        Returns:
            The Post object

        """

        if not self.obj:
            self.obj = Post()

        self.populate_obj(self.obj)
        self.obj.tags = [get_or_create(Tag, name=tag)[0] for tag in self.tags.data]
        return self.obj.save()

    def populate_obj(self, obj):
        for name, field in self._fields.items():
            if name not in ('next', 'tags'):
                field.populate_obj(obj, name)
