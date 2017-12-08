from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import Required

class NameForm(FlaskForm):
    '''username = StringField('昵称：',validators = [Required()])
    email = StringField('邮箱名：', validators = [Required()])
    password = PasswordField('密码', validators = [Required()])'''

    name = StringField('你是？', validators=[Required()])
    submit = SubmitField('登录')

