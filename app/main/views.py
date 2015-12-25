from flask import Blueprint, render_template, redirect, url_for, current_app
from sqlalchemy import desc

from app.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
@main.route('/index/<int:page>')
def index(page=1):
    posts = Post.query.order_by(desc(Post.timestamp)).paginate(
                page, current_app.config.get('POSTS_PER_PAGE'))

    return render_template('main/index.html', title='Home', posts=posts)


@main.route('/post/<int:id>')
@main.route('/post/<int:id>/<slug>')
def show_post(id, slug=None):
    post = Post.query.get_or_404(id)
    if slug is None:
        return redirect(url_for('main.show_post', id=id, slug=post.slug))

    return render_template('main/post.html', post=post)

# TODO: Tag page and search
