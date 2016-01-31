from wtforms import ValidationError

from app import db
from app.main.models import Tag
from app.admin.models import User
from app.admin.forms import PostForm, SettingsForm, UserForm
from tests import AppTestCase, DummyPostData


class TestPostForm(AppTestCase):
    def test_save(self):
        form_1 = PostForm(DummyPostData(title='foo', short_text='bar', tags='foo, bar, foo bar'))
        post_1 = form_1.save()
        tags_1 = Tag.query.all()

        self.assertListEqual(tags_1, post_1.tags.all())

        form_2 = PostForm(DummyPostData(title='foo', short_text='bar', tags='foo, bar, someothertag'))
        form_2.save()

        # Assert that only a single tag ('someothertag') has been added
        self.assertEqual(len(Tag.query.all()), 4)

        form_3 = PostForm(obj=post_1)
        form_3.tags.data = ['foo', 'bar', 'baz', 'duplicate', 'duplicate']
        form_3.save()

        tag_1 = Tag.query.filter_by(name='baz').first()
        tag_2 = Tag.query.filter_by(name='foo bar').first()

        self.assertIsNotNone(tag_1)
        self.assertNotIn(tag_2, post_1.tags.all())
        # Assert that the 'duplicate' tag has only been added once
        self.assertEqual(Tag.query.filter_by(name='duplicate').count(), 1)


class TestSettingsForm(AppTestCase):
    def test_initialization(self):
        form = SettingsForm()

        # Loop over each setting and assert that the field with the corresponding name has the same value
        for key, value in self.app.config['SETTINGS'].items():
            if key == 'installed':
                continue

            field = getattr(form, key)

            self.assertEqual(field.data, value)

    def test_save(self):
        form = SettingsForm()
        form.blog_name.data = 'foobar'
        form.save()

        self.assertEqual(self.app.config['SETTINGS']['blog_name'], 'foobar')


class TestUserForm(AppTestCase):
    def test_save(self):
        form = UserForm(DummyPostData(email='foo@bar.com', name='Foo Bar', password='foobar'))
        form.save()

        user = User.query.first()

        self.assertEqual(user.email, 'foo@bar.com')
        self.assertEqual(user.name, 'Foo Bar')
        self.assertNotEqual(user.password, 'foobar')

    def test_email_validation(self):
        user = User(email='foo@bar.com', name='Foo Bar', password='foobar')
        db.session.add(user)
        db.session.commit()

        form = UserForm(DummyPostData(email='foo@bar.com', name='Foo Baz', password='foobaz'))

        self.assertFalse(form.validate())

        form = UserForm(DummyPostData(email='foo@bar.com', name='Foo Baz', password='foobaz'), obj=user)

        self.assertTrue(form.validate())
