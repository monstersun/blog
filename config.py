import os

'''python中os.path.dirname的作用要看文件运行的方式，若是绝对路径运行则返回路径否则是空值'''
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USERNAME = 'sxyzztx@126.com'
    MAIL_PASSWORD = 'sunaiding750'
    MAIL_SUBJECT_PREFIX = '[Flasky]'
    MAIL_SENDER = 'FLASKY ADMIN <sxyzztx@126.com>'
    MAIL_DEBUG = True
    MAIL_TLS_USE = True
    FLASKY_ADMIN = 'sxyzztx@outlook.com'

    @staticmethod
    def init_app(app):
        pass
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/database-dev'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/database-dev'

class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/database-dev'

config = {
    'development': DevConfig,
    'testing': TestConfig,
    'product': ProductConfig,
    'default': DevConfig
}