from app import db, cache
from app.admin.models import Setting
from tests.general import AppTestCase


class TestAppSettings(AppTestCase):
    def test_setitem(self):
        self.app.config['SETTINGS']['foo'] = 'bar'
        setting = Setting.query.filter_by(name='foo').first()

        self.assertEqual(setting.value, 'bar')

        self.app.config['SETTINGS']['foo'] = 'foobar'

        self.assertEqual(setting.value, 'foobar')

    def test_getitem(self):
        setting = Setting(name='foo', value='bar')
        db.session.add(setting)
        db.session.commit()

        # We need to delete the Setting dictionary cache manually,
        # since we didn't add the setting through the AppSettings interface
        cache.delete_memoized(Setting.as_dict)

        self.assertEqual(self.app.config['SETTINGS']['foo'], 'bar')
