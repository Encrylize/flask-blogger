#!/usr/bin/env python

import os

import coverage
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask_security.utils import encrypt_password

from app import create_app, db, user_datastore
from app.main.models import Post, Tag
from app.admin.models import User, Setting
from config import basedir

app = create_app(os.getenv('CONFIG', 'default'))

migrate = Migrate(app, db)
manager = Manager(app)


def make_shell_context():
    """ Creates the shell context for the manager. """

    return dict(app=app, db=db, Post=Post, Tag=Tag, User=User, Setting=Setting)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

cov = coverage.coverage(branch=True, include='app/*')


@manager.command
def test(coverage=False):
    """ Runs the unit tests. """

    if coverage:
        cov.start()

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    if coverage:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        cov_dir = os.path.join(basedir, 'tmp/coverage')
        cov.html_report(directory=cov_dir)
        print('HTML version: %s/index.html' % cov_dir)
        cov.erase()


@manager.command
def createadmin(email, name, password):
    """ Creates an admin user. """
    password = encrypt_password(password)
    user = User(email=email, name=name, password=password, active=True)
    user.save()


if __name__ == '__main__':
    manager.run()
