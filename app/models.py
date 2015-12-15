from datetime import datetime

from app import db

# TODO: Add User model
tags_posts = db.Table('tags_posts',
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(10000), nullable=False)
    timestamp = db.Column(db.DateTime)
    tags = db.relationship('Tag', secondary=tags_posts, lazy='dynamic',
                           backref=db.backref('posts', lazy='dynamic'))

    # TODO: Once a User model has been added,
    # TODO: create an author relationship.
    # String placeholders for now
    author = db.Column(db.String())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Post %d>' % self.id


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

    def __repr__(self):
        return '<Tag %d>' % self.id
