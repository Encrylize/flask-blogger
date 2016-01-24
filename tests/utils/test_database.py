from app import db
from app.utils.database import CRUDMixin
from tests.general import AppTestCase


class TestCRUDMixin(AppTestCase):
    class DummyModel(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)

    def test_save(self):
        dummy_model = self.DummyModel()
        dummy_model.save()

        self.assertIsNotNone(self.DummyModel.query.first())

    def test_delete(self):
        dummy_model = self.DummyModel()
        db.session.add(dummy_model)
        db.session.commit()
        dummy_model.delete()

        self.assertIsNone(self.DummyModel.query.first())
