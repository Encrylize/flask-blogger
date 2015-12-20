from flask_pagedown.fields import PageDownField
from wtforms.fields import StringField
from wtforms.validators import DataRequired

from app.models import Post, Tag
from app.utils.helpers import get_or_create
from app.utils.forms import RedirectForm
from app.utils.fields import TagListField


class PostForm(RedirectForm):
    title = StringField('Title', [DataRequired()])
    body = PageDownField('Body', [DataRequired()])
    tags = TagListField('Tags (separated by comma)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = kwargs.get('obj')

    def save(self):
        if not self.obj:
            self.obj = Post()

        self.populate_obj(self.obj)
        self.obj.tags = [get_or_create(Tag, name=tag)[0] for tag in self.tags.data]
        self.obj.save()

    def populate_obj(self, obj):
        for name, field in self._fields.items():
            if name not in ('next', 'tags'):
                field.populate_obj(obj, name)
