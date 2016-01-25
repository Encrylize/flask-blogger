from flask import session, current_app
from wtforms.fields import StringField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import DataRequired, ValidationError

from app.admin.models import Setting
from app.main.models import Post, Tag
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
        self.post = kwargs.get('obj', Post())

        for field, value in session.pop('post_preview', {}).items():
            self._fields[field].data = value

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

        self.populate_obj(self.post)
        self.post.tags = [get_or_create(Tag, name=tag)[0] for tag in set(self.tags.data)]
        return self.post.save()

    def populate_obj(self, obj):
        for name, field in self._fields.items():
            if name not in ('next', 'tags'):
                field.populate_obj(obj, name)


class SettingsForm(RedirectForm):
    def __init__(self, *args, **kwargs):
        kwargs.update(dict(current_app.config['SETTINGS']))
        super().__init__(*args, **kwargs)

    @classmethod
    def configure(cls):
        """ Adds all settings with a name as form fields. """

        for setting in Setting.query.all():
            if setting.name is None:
                continue

            FieldType = {int: IntegerField,
                         str: StringField,
                         bool: BooleanField}[type(setting.value)]
            validators = {int: [DataRequired()],
                          str: [DataRequired()],
                          bool: []}[type(setting.value)]
            setattr(cls, setting.key, FieldType(setting.name, validators))

    def save(self):
        """ Saves the settings. """

        self.populate_obj(current_app.config['SETTINGS'])

    def validate_posts_per_page(self, field):
        if field.data < 1:
            raise ValidationError('This field must have a value of at least 1.')
