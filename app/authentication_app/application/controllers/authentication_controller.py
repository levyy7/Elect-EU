"""
Module: authentication_controller.py
Description: This module defines the authentication routes for user registration, 
retrieving user secrets, and verifying two-factor authentication (2FA) in the Flask application.

Routes:
1. /register: POST endpoint to register a new user and initiate 2FA setup.
2. /user_secrets: GET endpoint to retrieve all user secrets.
3. /verify-2fa: POST endpoint to verify the 2FA code and generate a JWT token.
"""

from flask import Blueprint, request, jsonify
from flask_injector import inject
from ..services.authentication_service import AuthenticationService
import jwt
import datetime

# Create a Blueprint for authentication-related routes
blueprint_authentication = Blueprint("authentication", __name__)


@blueprint_authentication.route("/register", methods=["POST"])
@inject
def register(authentication_service: AuthenticationService):
    """
    Handles user registration and initiates 2FA setup.

    Args:
        authentication_service: An instance of AuthenticationService for handling authentication logic.

    Returns:
        A JSON response indicating the result of the registration, 
        including the 2FA secret if successful or an error message.

    HTTP Status Codes:
        201: Registration successful.
        400: Missing email or password.
        401: Invalid email or password.
        500: Internal server error.
    """
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if not authentication_service.check_credentials(email, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate and send the initial code for 2FA setup
    try:
        secret = authentication_service.generate_2fa(email)
        return (
            jsonify(
                {
                    "message": "Registration successful, scan the QR code in Google Authenticator",
                    "secret": secret,
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@blueprint_authentication.route("/user_secrets", methods=["GET"])
@inject
def get_all_user_secrets(authentication_service: AuthenticationService):
    """
    Retrieves all user secrets from the database.

    Args:
        authentication_service: An instance of AuthenticationService for handling authentication logic.

    Returns:
        A JSON response containing the list of user secrets or an error message.

    HTTP Status Codes:
        200: Successfully retrieved user secrets.
        500: Internal server error.
    """
    try:
        user_secrets = authentication_service.get_all_user_secrets()
        return jsonify(user_secrets), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@blueprint_authentication.route("/verify-2fa", methods=["POST"])
@inject
def verify(authentication_service: AuthenticationService):
    """
    Verifies the 2FA code provided by the user and generates a JWT token upon successful verification.

    Args:
        authentication_service: An instance of AuthenticationService for handling authentication logic.

    Returns:
        A JSON response indicating the result of the verification, 
        including a JWT token if successful or an error message.

    HTTP Status Codes:
        200: 2FA verification successful, with a JWT token.
        400: Missing email or 2FA code, or invalid 2FA code.
        500: Internal server error.
    """
    user_id = request.json.get("user_id")
    email = request.json.get("email")
    code = request.json.get("code")

    if not email or not code:
        return jsonify({"error": "Email and 2FA code are required"}), 400

    try:
        is_valid = authentication_service.verify_2fa(email, code)
        if is_valid:
            # Generate JWT token
            token = jwt.encode(
                {
                    "user_id": user_id,
                    "email": email,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                },
                "your_secret_key",  # Replace this with your actual secret key
                algorithm="HS256",
            )
            return (
                jsonify({"message": "2FA verification successful", "token": token}),
                200,
            )
        else:
            return jsonify({"error": "Invalid 2FA code"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
