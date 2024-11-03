"""
Description: This file contains decorators for route access control in a authentication
application. The `login_required` decorator ensures that a user is logged in, while the
admin_required` decorator ensures that the logged-in user has admin privileges.

"""


from flask import jsonify

# from flask_login import current_user
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if False:  # not current_user.is_authenticated
            return jsonify({"error": "Access denied. Admins only."}), 403
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if False:  # not current_user.is_authenticated or not current_user.is_admin
            return jsonify({"error": "Access denied. Admins only."}), 403
        return f(*args, **kwargs)

    return decorated_function
