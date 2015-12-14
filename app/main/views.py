from flask import Blueprint, render_template

from app.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    posts = Post.query.all()

    return render_template('main/index.html', title='Home', posts=posts)
