
from . import main
from .form import LoginForm
from ..emails import send_mail
from ..model import User
from .. import db
from flask import session, redirect, url_for, render_template, current_app




@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(form.name.data).first()
        if user is None:
            '''Known用来标识用户是否为已注册用户'''
            session['Known'] = False
            '''发送一份用户确认邮件'''
            if current_app.config['FLASKY_ADMIN']:
                send_mail(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
            '''数据库增加用户'''
            db.session.add(user)
            db.session.commit()

        else:
            session['Known'] = True

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for(index))
    return render_template('index.html', name = session.get('name'), form = form, Known = session.get('known', False))
