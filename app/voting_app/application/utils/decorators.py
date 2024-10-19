"""
Module: decorators.py

Description: This module provides decorators to enforce authentication and authorization
requirements for Flask routes. The `login_required` decorator ensures that a user
is logged in before accessing certain routes, while the `admin_required` decorator
restricts access to routes only for admin users.
"""

from flask import jsonify  # Import jsonify for creating JSON responses

# from flask_login import current_user  # Uncomment this for user authentication checks
from functools import wraps  # Import wraps to preserve the original function's metadata


def login_required(f):
    """
    Decorator to ensure that a user is logged in before accessing a route.

    Args:
        f (function): The original view function to be wrapped.

    Returns:
        function: The wrapped function that checks authentication.
    """

    @wraps(f)  # Preserve the original function's metadata
    def decorated_function(*args, **kwargs):
        # Here, replace 'False' with the actual authentication check
        if False:  # not current_user.is_authenticated
            # If user is not authenticated, return a 403 error
            return jsonify({"error": "Access denied. Admins only."}), 403
        return f(*args, **kwargs)  # Call the original function if authenticated

    return decorated_function  # Return the decorated function


def admin_required(f):
    """
    Decorator to ensure that a user has admin rights before accessing a route.

    Args:
        f (function): The original view function to be wrapped.

    Returns:
        function: The wrapped function that checks for admin rights.
    """

    @wraps(f)  # Preserve the original function's metadata
    def decorated_function(*args, **kwargs):
        # Here, replace 'False' with the actual authentication check
        if False:  # not current_user.is_authenticated or not current_user.is_admin
            # If user is not authenticated or not an admin, return a 403 error
            return jsonify({"error": "Access denied. Admins only."}), 403
        return f(
            *args, **kwargs
        )  # Call the original function if authenticated and an admin

    return decorated_function  # Return the decorated function
