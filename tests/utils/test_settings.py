from app.models import Setting
from tests.general import AppTestCase


class TestAppSettings(AppTestCase):
    def test_setting_creation(self):
        self.app.config['SETTINGS']['foo'] = 'bar'
        setting = Setting.query.filter_by(name='foo').first()
        self.assertEqual(setting.value, 'bar')

        self.app.config['SETTINGS']['foo'] = 'foobar'
        self.assertEqual(setting.value, 'foobar')
