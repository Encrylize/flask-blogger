from flask import Blueprint, render_template, redirect, url_for
from flask_security import current_user

admin = Blueprint('admin', __name__)


@admin.route('/')
@admin.route('/index')
def index():
    return render_template('admin/index.html', title='Admin')


@admin.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('security.login', next='admin'))
