from flask import render_template, redirect, url_for, current_app, g
from sqlalchemy import desc

from app import db
from app.main import main
from app.main.forms import SearchForm
from app.admin.models import User
from app.main.models import Post, Tag, tags_posts


@main.route('/')
@main.route('/index')
@main.route('/index/<int:page>')
def index(page=1):
    posts = Post.query.order_by(desc(Post.timestamp)).paginate(
                page, current_app.config['SETTINGS']['posts_per_page'])

    return render_template('main/post_previews.html', title='Home', header='Posts', posts=posts)


@main.route('/post/<int:id>')
@main.route('/post/<int:id>/<slug>')
def show_post(id, slug=None):
    post = Post.query.get_or_404(id)
    if slug is None:
        return redirect(url_for('main.show_post', id=id, slug=post.slug))

    return render_template('main/post.html', title=post.title, post=post)


@main.route('/tag/<int:id>')
@main.route('/tag/<int:id>/<slug>')
@main.route('/tag/<int:id>/<slug>/<int:page>')
def show_tag(id, slug=None, page=1):
    tag = Tag.query.get_or_404(id)
    if slug is None:
        return redirect(url_for('main.show_tag', id=id, slug=tag.slug))

    posts = tag.posts.order_by(desc(Post.timestamp)).paginate(
                page, current_app.config['SETTINGS']['posts_per_page'])

    return render_template('main/post_previews.html', title=tag.name,
                           header='Posts tagged with "%s":' % tag.name, posts=posts)


@main.route('/user/<int:id>')
@main.route('/user/<int:id>/<slug>')
@main.route('/user/<int:id>/<slug>/<int:page>')
def show_user(id, slug=None, page=1):
    user = User.query.get_or_404(id)
    if slug is None:
        return redirect(url_for('main.show_user', id=id, slug=user.slug))

    posts = user.posts.order_by(desc(Post.timestamp)).paginate(
                page, current_app.config['SETTINGS']['posts_per_page'])

    return render_template('main/post_previews.html', title=user.name,
                           header='Posts by %s:' % user.name, posts=posts)


@main.route('/search', methods=['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('main.index'))

    return redirect(url_for('main.show_search_results', query=g.search_form.search_field.data))


@main.route('/search_results/<query>')
@main.route('/search_results/<query>/<int:page>')
def show_search_results(query, page=1):
    posts = Post.query.whoosh_search(query).order_by(desc(Post.timestamp)).paginate(
                page, current_app.config['SETTINGS']['posts_per_page'])

    return render_template('main/post_previews.html', title='Search results',
                           header='Search results for %s:' % query, posts=posts)


@main.context_processor
def inject_tags():
    tags = Tag.query.join(tags_posts).group_by(Tag).order_by(desc(db.func.count(tags_posts.c.post_id))).all()
    return dict(tags=tags)


@main.before_request
def set_globals():
    g.search_form = SearchForm()
