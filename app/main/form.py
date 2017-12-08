from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from ..model import Role, User

class NameForm(FlaskForm):
    '''username = StringField('昵称：',validators = [Required()])
    email = StringField('邮箱名：', validators = [Required()])
    password = PasswordField('密码', validators = [Required()])'''

    name = StringField('你是？', validators=[Required()])
    submit = SubmitField('登录')

class EditProfileForm(FlaskForm):
    realname = StringField('真实姓名', validators=[Required(), Length(1, 64)])
    location = StringField('地址', validators=[Required(), Length(1,64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
    username = StringField('用户名', validators=[Required(), Regexp('^[A-Z][A-Za-z_.]*$', 0, '用户名必须是字母下划线组成')])
    confirmed = BooleanField('确认')
    role = SelectField('选择角色', coerce=True)
    name = StringField('真实姓名', validators=[Length(1,128)])
    location = StringField('地址')
    about_me = StringField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(self, *args, **kwargs)
        self.user = user
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            return ValidationError('邮箱已注册')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            return ValidationError('用户名已注册')



