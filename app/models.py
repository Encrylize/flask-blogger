from datetime import datetime

from app import db

# TODO: Add Tag and User model


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(10000), nullable=False)
    timestamp = db.Column(db.DateTime)

    # TODO: Once a Tag and User model has been added,
    # TODO: create an author relationship and tag relationship.
    # String placeholders for now
    author = db.Column(db.String())
    tags = db.Column(db.String())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Post %d>' % self.id
