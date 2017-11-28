from . import auth
from .form import LoginForm
from ..model import User
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.vertify(form.password.data):
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

