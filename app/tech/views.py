from flask import render_template, redirect, url_for, request
from .form import PostForm
from ..model import User, TechPost
from . import tech
from .. import db

@tech.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = TechPost.query.order_by(TechPost.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    techposts = pagination.items
    return render_template('tech/index.html', techposts =techposts)

@tech.route('/show/<int:id>')
def show(id):
    post = TechPost.query.get_or_404(id)
    return render_template('tech/postShow.html', post=post)

@tech.route('/write', methods=['GET', 'POST'])
def write():
    form = PostForm()
    if form.validate_on_submit():
        post = TechPost(title=form.title.data,
                        summary=form.summary.data,
                        body=form.body.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('tech.index'))
    return render_template('tech/write.html', form=form)