from . import main
from flask import render_template, abort, redirect, url_for, request
from ..model import User, Role, Permission, Post
from .form import EditProfileForm, EditProfileAdminForm, PostForm
from flask_login import login_required, current_user
from .. import db
from ..deractors import permission_required, admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit() and current_user.can(Permission.WRITE_ARITICLES):
        post = Post(body=form.body.data, auther=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


'''用户资料管理器'''
@main.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.realname.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('editprofile.html', form=form)


'''管理员级别的用户资料管理器'''
@main.route('/editprofile/<int:id>', methods=['GET', 'POST'])
@login_required
def editadmin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.name = form.name.data
        #这个地方一定要注意定义了外键的columns，一般user.role是个对象，此处用user.role = form.role.data, 用int赋进对象是不对的
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about_me = form.about_me.data

        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.name.data = user.name
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.about_me

    return render_template('editprofile.html', form=form)
