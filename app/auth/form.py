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
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('邮箱已注册')
    '''验证用户名唯一性'''
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已存在')

'''修改密码表单（找回密码也可用）'''
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('您的旧密码', validators=[Required()])
    password = PasswordField('您的新密码：', validators=[Required(), EqualTo('password2', '新密码与确认密码不一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('提交')

'''找回密码邮箱表单'''
class PasswordResetEmailForm(FlaskForm):
    email = StringField('请输入您的邮箱', validators=[Required(), Length(1,64), Email()])
    submit = SubmitField('提交')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('邮箱不存在')

class PasswordResetFrom(FlaskForm):
    email = StringField('请输入你的邮箱', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('输入您的新密码', validators=[Required(), EqualTo('password2', '密码不一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('提交')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('邮箱不存在')
