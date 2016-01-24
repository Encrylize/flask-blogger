from datetime import datetime

from slugify import slugify
from sqlalchemy import event
from sqlalchemy.orm import Session

from app import db
from app.utils.database import CRUDMixin

tags_posts = db.Table('tags_posts',
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete='cascade')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='cascade')))


class Post(db.Model, CRUDMixin):
    __searchable__ = ['title', 'short_text', 'long_text']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    short_text = db.Column(db.String(1000))
    long_text = db.Column(db.String(10000))
    timestamp = db.Column(db.DateTime)
    slug = db.Column(db.String(160))
    tags = db.relationship('Tag', secondary=tags_posts, lazy='dynamic',
                           backref=db.backref('posts', lazy='dynamic'))
    post_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    __table_args__ = (db.CheckConstraint('NOT(short_text IS NULL AND long_text IS NULL)'),)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.utcnow()

    def save(self):
        """
        Creates the slug and saves the post.

        Returns:
            The Post object

        """

        self.slug = slugify(self.title)
        return super().save()


class Tag(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    slug = db.Column(db.String(80), nullable=False)


@event.listens_for(Session, 'after_flush')
def delete_tag_orphans(session, ctx):
    """ Deletes all Tag objects with no posts. """

    session.query(Tag).filter(~Tag.posts.any()).delete(synchronize_session=False)


def before_tag_insert_listener(mapper, connection, target):
    """ Creates the slug for a Tag object. """

    target.slug = slugify(target.name)

event.listen(Tag, 'before_insert', before_tag_insert_listener)
