from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_security import current_user

from app.models import Post

admin = Blueprint('admin', __name__)


@admin.route('/')
@admin.route('/index')
def index():
    return render_template('admin/index.html', title='Admin')


@admin.route('/posts')
@admin.route('/posts/<int:page>')
def show_posts(page=1):
    posts = Post.query.paginate(page, current_app.config.get('POSTS_PER_PAGE', 20))
    return render_template('admin/posts.html', posts=posts)


@admin.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('security.login', next='admin'))
