from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, ValidationError
from ..model import User

class LoginForm(FlaskForm):

    email = StringField('邮件', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[Required()])
    remeber_me = BooleanField('记住我')
    submit = SubmitField('登陆')


class RegisterForm(FlaskForm):

    email = StringField('您的邮箱：', validators=[Required(), Length(1,64), Email()])
    username = StringField('您的用户名', validators=[Required(), Length(1,64),
                                                 Regexp('^[A-Z a-z][A-Za-z0-9_.]*$', 0,
                                                        '用户名只能是字母数字还有下划线及小数点')])
    password = PasswordField('您的密码', validators=[Required(), EqualTo('password2',
                                                                     '密码和确认密码必须一致')])
    password2 = PasswordField('确认密码', validators=[Required()])

    submit = SubmitField('注册')

    '''验证邮箱唯一性，注意方法名必须为validate_+字段名'''
    def validate_email(self, field):
        if User.query.filter_by(email = field.data):
            raise ValidationError('邮箱已注册')
    '''验证用户名唯一性'''
    def validate_username(self, field):
        if User.query.filter_by(username = field.data):
            raise ValidationError('用户名已存在')