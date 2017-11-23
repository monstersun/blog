from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import Required


'''初始化flask'''
app = Flask(__name__)
'''初始化bootstrap'''
bootstrap = Bootstrap(app)
'''秘钥'''
app.config['SECRET_KEY'] = 'hard to guess string'
'''新建表单类'''
class NameForm(FlaskForm):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')


'''主页'''
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name.')
        session['name'] = form.name.data

        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'))



if __name__ == '__main__':
    app.run()