from datetime import datetime

from flask_security import UserMixin, RoleMixin
from slugify import slugify

from app import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')))
tags_posts = db.Table('tags_posts',
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


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
    body = db.Column(db.String(10000), nullable=False)
    timestamp = db.Column(db.DateTime)
    slug = db.Column(db.String(160))
    tags = db.relationship('Tag', secondary=tags_posts, lazy='dynamic',
                           backref=db.backref('posts', lazy='dynamic'))
    post_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.utcnow()

    def save(self):
        slug = slugify(self.title)

        if Post.query.filter_by(slug=slug).first():
            version = 2
            while True:
                new_slug = '%s%d' % (slug, version)
                if Post.query.filter_by(slug=new_slug).first() is None:
                    slug = new_slug
                    break
                version += 1

        self.slug = slug

        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Post %d>' % self.id


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))

    def __repr__(self):
        return '<Tag %d>' % self.id
