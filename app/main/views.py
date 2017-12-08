from . import main
from flask import render_template, abort, redirect, url_for
from ..model import User
from .form import EditProfileForm, EditProfileAdminForm
from flask_login import login_required, current_user
from .. import db
from ..deractors import permission_required, admin_required



@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

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

@main.route('/editprofile/<int:id>', methods=['GET', 'POST'])
@login_required
def editadmin(id):
    user = User.query.getor404(id=id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.name = form.name.data
        user.role = form.role.data
        user.location = form.location.data
        user.about_me = form.about_me.data

        return redirect(url_for('main.user'))
    form.email.data = user.email
    form.username.data = user.username
    form.name.data = user.name
    form.role.data = user.role
    form.location.data = user.location
    form.about_me.data = user.about_me

    return render_template('editprofile.html', form=form)
