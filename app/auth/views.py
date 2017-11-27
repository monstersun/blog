from . import auth
from .form import LoginForm
from ..model import User
from flask import render_template, redirect, url_for
from flask_login import login_user
form = LoginForm()

@auth.route('/login')
def login():
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.vertify(form.password.data):
            login_user(user, form.remeber_me.data)
            return redirect(url_for('index'))