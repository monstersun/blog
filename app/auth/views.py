from . import auth
from .form import LoginForm, RegisterForm, ChangePasswordForm
from ..model import User
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .. import db
from ..emails import send_mail

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)

            '''request.args.get('next')中的next指的是原本要访问但没有权限导致登录的原网页'''
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户不存在或者密码错误')
    return render_template('./auth/login.html', form = form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已登出')
    return redirect(url_for('main.index'))

'''注册页面'''
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'auth/emails/confirm', user=user, token=token)
        flash('A confirm email has been sent to your emailbox')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

'''用户确认'''
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return  redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('确认完毕！感谢您的配合')
    else:
        flash('确认连接已经失效')
    return redirect(url_for('main.index'))

'''拦截未确认用户'''
@auth.before_app_request
def before_request():
    if current_user.is_authenticated and\
             not current_user.confirmed\
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirm'))

@auth.route('/unconfirm')
def unconfirm():
    if current_user.is_anonymous and current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirm.html')


'''再次发送确认邮件'''
@auth.route('/confirm')
def resend_confirm_email():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, 'auth/emails/confirm', user=current_user, token=token)
    flash('新的确认邮件已发送')
    return redirect('main.index')

'''修改密码'''
@auth.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.change_password(form.password.data)
            return redirect(url_for('auth.login'))
    return render_template('auth/changePassword.html', form = form)



        

