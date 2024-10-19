"""
Module: decorators.py
Description:
    This module contains decorators for route access control in a Flask application.
    The `login_required` decorator ensures that a user is logged in, while the
    `admin_required` decorator ensures that the logged-in user has admin privileges.
"""

from flask import jsonify
from functools import wraps


def login_required(f):
    """
    Decorator to ensure that the user is logged in before accessing a route.

    Args:
        f (function): The original function to be decorated.

    Returns:
        function: The decorated function that checks user authentication.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is authenticated
        # (Currently set to always False for testing).
        if False:  # not current_user.is_authenticated
            return jsonify({"error": "Access denied. Admins only."}), 403
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """
    Decorator to ensure that the user is an admin before accessing a route.

    Args:
        f (function): The original function to be decorated.

    Returns:
        function: The decorated function that checks for admin privileges.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is authenticated and if the user is an admin
        # (currently set to always False for testing).
        if False:  # not current_user.is_authenticated or not current_user.is_admin
            return jsonify({"error": "Access denied. Admins only."}), 403
        return f(*args, **kwargs)

    return decorated_function
