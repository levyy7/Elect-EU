from flask import jsonify
from flask_login import current_user
from functools import wraps


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"error": "Access denied. Admins only."}), 403
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({"error": "Access denied. Admins only."}), 403
        return f(*args, **kwargs)

    return decorated_function
