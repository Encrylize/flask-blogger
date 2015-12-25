from flask import Blueprint, render_template, redirect, url_for, current_app, flash
from flask_security import current_user

from app import db
from app.models import Post
from app.admin.forms import PostForm
from app.utils.helpers import get_redirect_target

admin = Blueprint('admin', __name__)


@admin.route('/')
@admin.route('/index')
def index():
    return render_template('admin/index.html', title='Admin')


@admin.route('/posts')
@admin.route('/posts/<int:page>')
def show_posts(page=1):
    posts = Post.query.paginate(page, current_app.config.get('POSTS_PER_PAGE'))
    return render_template('admin/posts.html', posts=posts)


@admin.route('/new/post', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        form.save()
        flash('Added post.', 'success')

        return form.redirect(url_for('admin.index'))

    return render_template('admin/post_form.html', form=form)

@admin.route('/edit/post/<int:id>')
@admin.route('/edit/post/<int:id>/<slug>', methods=['GET', 'POST'])
def edit_post(id, slug=None):
    post = Post.query.get_or_404(id)
    if slug is None:
        return redirect(url_for('admin.edit_post', id=id, slug=post.slug))

    form = PostForm(obj=post)
    if form.validate_on_submit():
        form.save()
        flash('Edited post.', 'success')

        return form.redirect(url_for('admin.index'))

    return render_template('admin/post_form.html', form=form)


@admin.route('/delete/post/<int:id>')
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Deleted post.', 'success')

    return redirect(get_redirect_target() or url_for('admin.index'))


@admin.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('security.login', next='admin'))
