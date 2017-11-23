from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

'''实例化扩展类'''
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
moment = Moment

'''定义工厂函数'''
def cerate_app(config_name):
    '''初始化flaskapp'''
    app = Flask(__name__)
    '''初始化扩展对象'''
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    moment.init_app(app)

    '''注册蓝本'''
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app