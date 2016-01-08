from app import db


class CRUDMixin:
    def save(self):
        """ Saves the instance and returns it. """

        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """ Deletes the instance."""

        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<%s %d>' % (self.__class__.__name__, self.id)
