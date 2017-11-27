from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email

class LoginForm(FlaskForm):

    email = StringField('邮件', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('密码')
    remeber_me = BooleanField('记住我')
    submit = SubmitField('登陆')
