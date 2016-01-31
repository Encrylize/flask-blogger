from flask import session, current_app
from flask_security import current_user
from flask_security.utils import encrypt_password
from wtforms.fields import StringField, TextAreaField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Email

from app.admin.models import User, Setting
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

    def save(self, set_author=False):
        """
        Saves the Post object.

        Args:
            set_author: If True, the author of the post is set to the current user.

        Returns:
            The Post object

        """

        if set_author:
            self.post.author = current_user

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


class UserForm(RedirectForm):
    email = StringField('Email', [DataRequired(), Email()])
    name = StringField('Name', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('obj', User())

    def save(self):
        """
        Saves the User object.

        Returns:
            The User object

        """

        self.populate_obj(self.user)
        self.user.active = True
        self.user.password = encrypt_password(self.password.data)
        return self.user.save()

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None and user != self.user:
            raise ValidationError('A user with this email already exists.')
