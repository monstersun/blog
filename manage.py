from flask import Flask, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import Required
from flask_mail import Mail, Message
from flask_script import Manager,Shell
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from threading import Thread

'''初始化flask'''
app = Flask(__name__)
'''初始化bootstrap'''
bootstrap = Bootstrap(app)
'''秘钥'''
app.config['SECRET_KEY'] = 'hard to guess string'


'''flask配置信息'''
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sxyzztx@126.com'
app.config['MAIL_PASSWORD'] = 'sunaiding512'
app.config['MAIL_DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:126.com@localhost/data-test'
app.config['SQLALCHEMY_COMMIT_ON_TERADOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SUBJECT_PREFIX'] = '[FLASKY]'
app.config['MAIL_SENDER'] = 'FLASKY ADMIN <sxyzztx@126.com>'
'''初始化db类'''
db = SQLAlchemy(app)

'''定义表类'''
'''roles表'''
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref = 'role')

    def __repr__(self):
        return '<Role, %r>' % self.name


'''users表'''
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User %r' % self.username

'''初始化mail类'''
mail = Mail(app)

'''新建表单类'''
class NameForm(FlaskForm):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')


'''邮件函数'''
def send_aysc_mail(msg, app):
    with app.app_context():
        mail.send(msg)

def mail_send(name,subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['MAIL_SENDER'], recipients=['sxyzztx@outlook.com'])
    msg.body = render_template(template + '.text', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_aysc_mail, args=[app, msg])
    thr.start()
    return thr


'''flask管理工具'''
manager = Manager(app)
def make_shell_context():
    return dict(app=app, User=User, Role=Role, db=db)
manager.add_command('shell', Shell(make_context=make_shell_context))
'''数据库迁移工具'''
migrate= Migrate(app, db)
manager.add_command('db', MigrateCommand)

'''主页'''
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data)
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        db.session.commit()
        session['name'] = form.name.data
        form.name.data = ''

        return redirect(url_for('index'))

    return render_template('index.html', form = form, name = session.get('name'), known = session.get('known', False))



if __name__ == '__main__':
    manager.run()