from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import Required

class LoginForm(FlaskForm):
    username = StringField('用户名/昵称：', validators=[Required])
    email = StringField('邮件', validators=[])
    password = PasswordField('密码')