from datetime import datetime

from flask_security import UserMixin, RoleMixin
from slugify import slugify
from sqlalchemy import event
from sqlalchemy.orm import Session, Mapper

from app import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')))
tags_posts = db.Table('tags_posts',
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete='cascade')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='cascade')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role %d>' % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %d>' % self.id


class Post(db.Model):
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
        db.session.add(self)
        db.session.commit()

        return self

    def __repr__(self):
        return '<Post %d>' % self.id


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    slug = db.Column(db.String(80))

    def __repr__(self):
        return '<Tag %d>' % self.id


@event.listens_for(Session, 'after_flush')
def delete_tag_orphans(session, ctx):
    session.query(Tag).filter(~Tag.posts.any()).delete(synchronize_session=False)


def before_tag_insert_listener(mapper, connection, target):
    target.slug = slugify(target.name)

event.listen(Tag, 'before_insert', before_tag_insert_listener)
