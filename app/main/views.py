from . import main
from flask import render_template, abort, redirect, url_for, request, flash, make_response
from ..model import User, Role, Permission, Post, Comment
from .form import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from flask_login import login_required, current_user
from .. import db
from ..deractors import permission_required, admin_required

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit() and current_user.can(Permission.WRITE_ARTICLES):
        post = Post(body=form.body.data, auther=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_post
    else:
        query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, show_followed=show_followed, posts=posts, pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)


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



'''文章编辑器'''
@main.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.auther and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

'''关注'''
@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('你已关注此用户')
        return redirect((url_for('user', username=user.username)))
    current_user.follow(user)
    flash('关注成功')
    return redirect(url_for('.user', username=user.username))

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("用户不存在")
        return redirect(url_for('index'))
    if not current_user.is_following(user):
        flash('未关注用户')
    current_user.unfollow(user)
    flash('取消成功')
    return redirect(url_for('.user', username=user.username))

@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page, per_page=20, error_out=False)
    follows = [{'user':item.follower, 'timestamp':item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title='Follows of', endpoint='.followers',
                           pagination=pagination, follows=follows)

@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, per_page=20, error_out=False)
    follows = [{'user':item.followed, 'timestamp':item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title='Followed by', endpoint='.followed',
                           pagination=pagination, follows=follows)


'''设置cookies'''
@main.route('/all')
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp

@main.route('/follow')
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=24*30*60*60)
    return resp


'''用户评论(文章)路由'''
@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.comments.data,
                         author=current_user._get_current_object(),
                         post=post)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1)//20 + 1
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    comments = pagination.items
    return render_template('post.html', comments=comments, pagination=pagination, posts=[post], form=form)

'''修改用户评论'''
@main.route('/moderate_comments')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments, pagination=pagination, page=page)

'''评论管理按钮'''
@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    return redirect(url_for('.moderate_comments', page=page))

@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_shut(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    return redirect(url_for('.moderate_comments', page=page))
