from flask import Blueprint, render_template, redirect, url_for

from app.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    posts = Post.query.all()

    return render_template('main/index.html', title='Home', posts=posts)


@main.route('/post/<int:id>')
@main.route('/post/<int:id>/<slug>')
def show_post(id, slug=None):
    post = Post.query.get_or_404(id)
    if slug is None:
        return redirect(url_for('main.show_post', id=id, slug=post.slug))

    return render_template('main/post.html', post=post)
