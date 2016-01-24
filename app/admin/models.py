from flask_security import UserMixin, RoleMixin

from app import cache, db
from app.utils.database import CRUDMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')


class Setting(db.Model, CRUDMixin):
    key = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.PickleType, nullable=False)

    @classmethod
    @cache.memoize()
    def as_dict(cls):
        return {setting.key: setting.value for setting in cls.query.all()}

    def __repr__(self):
        return '<Setting %s>' % self.key
