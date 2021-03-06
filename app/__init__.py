from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown

'''实例化扩展类'''
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
pagedown = PageDown()

login_manager.login_view = 'auth.login'

'''定义工厂函数'''
def create_app(config_name):
    '''初始化flaskapp'''
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    '''初始化扩展对象'''
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    '''注册蓝本'''
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    '''增加蓝本'''
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/auth')

    '''todolist蓝本'''
    from .todo import todolist
    app.register_blueprint(todolist, url_prefix='/todolist')

    '''tech技术博客蓝本'''
    from .tech import tech
    app.register_blueprint(tech, url_prefix='/tech')

    return app