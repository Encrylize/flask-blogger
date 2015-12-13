from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)


@admin.route('/')
@admin.route('/index')
def index():
    return render_template('admin/index.html', title='Admin')
