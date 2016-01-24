from app import db, cache
from app.admin.models import Setting
from tests import AppTestCase


class TestAppSettings(AppTestCase):
    def test_setitem(self):
        self.app.config['SETTINGS']['foo'] = 'bar'
        setting = Setting.query.filter_by(key='foo').first()

        self.assertEqual(setting.value, 'bar')

        self.app.config['SETTINGS']['foo'] = 'foobar'

        self.assertEqual(setting.value, 'foobar')

    def test_getitem(self):
        setting = Setting(key='foo', value='bar')
        db.session.add(setting)
        db.session.commit()

        self.assertEqual(self.app.config['SETTINGS']['foo'], 'bar')
