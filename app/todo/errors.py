from . import todolist
from flask import render_template

@todolist.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@todolist.errorhandler(500)
def interval_error(e):
    return render_template('500.html')