from . import todolist
from .form import ListForm
from ..model import List, Category, User
from .. import db
from flask import redirect, render_template, url_for, abort, flash
from flask_login import login_required, current_user

@todolist.route('/list/<int:id>', methods=['GET', 'POST'])
@login_required
def list(id):
    user = User.query.get_or_404(id)
    if user is None:
        abort(404)
    form = ListForm()
    if form.validate_on_submit():
        list = List(body=form.event.data, compeleted=False, category=Category.query.get(form.category.data),
                    owner=User.query.get(id),)
        db.session.add(list)
        db.session.commit()
        return redirect(url_for('todolist.list', id=user.id))
    lists = user.lists.order_by(List.timestamp.asc()).all()
    return render_template('todo/todolist.html', lists=lists, form=form)

@todolist.route('/list/compelete/<int:id>')
@login_required
def list_compelete(id):
    list = List.query.get_or_404(id)
    list.compeleted = True
    db.session.add(list)
    db.session.commit()
    return redirect(url_for('todolist.list', id=current_user.id))

@login_required
@todolist.route('/list/delete/<int:id>')
def list_delete(id):
    list = List.query.get_or_404(id)
    db.session.delete(list)
    db.session.commit()
    flash('有条每日任务被删除。')
    return redirect(url_for('todolist.list', id=current_user.id))

