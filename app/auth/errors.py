from . import auth
from flask import render_template

@auth.app_errorhandler(403)
def http_forbidden():
    return render_template('auth/403.html')