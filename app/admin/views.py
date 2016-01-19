from flask import Blueprint, render_template, redirect, url_for, current_app, flash, session, request
from flask_security import current_user
from sqlalchemy import desc

from app.models import Post, Tag, User
from app.admin.forms import PostForm, SettingsForm
from app.utils.helpers import get_redirect_target

admin = Blueprint('admin', __name__)


@admin.route('/')
@admin.route('/index')
def index():
    return render_template('admin/index.html', title='Admin')


@admin.route('/posts')
@admin.route('/posts/<int:page>')
def show_posts(page=1):
    posts = Post.query.order_by(desc(Post.timestamp)).paginate(
                page, int(current_app.config['SETTINGS']['posts_per_page']))
    return render_template('admin/posts.html', posts=posts)


@admin.route('/new/post', methods=['GET', 'POST'])
def new_post():
    form = PostForm(**session.pop('post_preview', {}))
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
    for field, value in session.pop('post_preview', {}).items():
        setattr(getattr(form, field), 'data', value)

    if form.validate_on_submit():
        form.save()
        flash('Edited post.', 'success')

        return form.redirect(url_for('admin.index'))

    return render_template('admin/post_form.html', form=form)


@admin.route('/delete/post/<int:id>')
def delete_post(id):
    post = Post.query.get_or_404(id)
    post.delete()
    flash('Deleted post.', 'success')

    return redirect(get_redirect_target() or url_for('admin.index'))


@admin.route('/preview', methods=['GET', 'POST'])
def preview_post():
    form = PostForm()
    session['post_preview'] = form.data
    post = Post(**{k: v for k, v in session['post_preview'].items() if k not in ('next', 'tags')})
    post.tags = [Tag(name=tag) for tag in form.tags.data]

    return render_template('admin/preview_post.html', post=post)


@admin.route('/settings', methods=['GET', 'POST'])
def edit_settings():
    form = SettingsForm(**dict(current_app.config['SETTINGS']))
    if form.validate_on_submit():
        form.populate_obj(current_app.config['SETTINGS'])
        flash('Updated settings.', 'success')
        return form.redirect(url_for('admin.index'))

    return render_template('admin/settings.html', form=form)


@admin.route('/users')
@admin.route('/users/<int:page>')
def show_users(page=1):
    users = User.query.paginate(page, int(current_app.config['SETTINGS']['posts_per_page']))
    return render_template('admin/users.html', users=users)


@admin.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('security.login', next='admin'))


@admin.after_request
def clear_post_preview(response):
    if request.endpoint != 'admin.preview_post':
        try:
            session.pop('post_preview')
        except KeyError:
            pass

    return response
