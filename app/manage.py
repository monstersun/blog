from flask import Flask, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import Required
from flask_mail import Mail, Message
from flask_script import Manager


'''初始化flask'''
app = Flask(__name__)
'''初始化bootstrap'''
bootstrap = Bootstrap(app)
'''秘钥'''
app.config['SECRET_KEY'] = 'hard to guess string'

'''flask管理工具'''
manager = Manager(app)

'''flask配置信息'''
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sxyzztx@126.com'
app.config['MAIL_PASSWORD'] = 'sunaiding512'
app.config['MAIL_DEBUG'] = True

'''初始化mail类'''
mail = Mail(app)

'''新建表单类'''
class NameForm(FlaskForm):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')

'''邮件函数'''
def mail_send(name):
    msg = Message('this is test e-mail', sender='sxyzztx@126.com', recipients=['sxyzztx@outlook.com'])
    msg.body = 'hello,%s'%name
    mail.send(msg)

'''主页'''
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        form.name.data = ''
        mail_send(session.get('name'))
        return redirect(url_for('index'))

    return render_template('index.html', form = form, name = session.get('name'))



if __name__ == '__main__':
    app.run()