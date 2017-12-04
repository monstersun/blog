from functools import wraps
from flask import abort
from .model import Permission
from flask_login import current_user


def permission_required(permission,f):

        @wraps(f)
        def decorator_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
                return f(*args, **kwargs)
        return decorator_function


def admin_required(f):
    return permission_required(Permission.ADMINISTER,f)(f)
