import os

'''python中os.path.dirname的作用要看文件运行的方式，若是绝对路径运行则返回路径否则是空值'''
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDWON = True