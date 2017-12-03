from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .  import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='roles')

    def __repr__(self):
        return 'Role, <%r>'%self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)


    '''密码加密hash'''
    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    '''验证密码'''
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    '''确认用户账户'''
    '''生成确认令牌'''
    def generate_confirmation_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm' : self.id})

    '''验证令牌'''
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


    '''修改密码'''
    def change_password(self, new_password):
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True


    '''找回密码'''
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'reset_confirm': self.id})

    def reset_confirm(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset_confirm') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True


    def __repr__(self):
        return 'User, %r'%self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))