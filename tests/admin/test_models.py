from app.admin.models import User
from tests import AppTestCase


class TestUser(AppTestCase):
    def test_save(self):
        user = User(email='foo@bar.com', name='Foo Bar ß', password='foobar')
        user.save()

        self.assertEqual(user.slug, 'foo-bar-ss')
