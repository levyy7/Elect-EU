"""
Description: This file defines the authentication routes for user registration,
retrieving user secrets, and verifying two-factor authentication (2FA)
in the authentification application.

"""


from flask import Blueprint, request, jsonify
from flask_injector import inject
from ..services.authentication_service import AuthenticationService
import jwt
import datetime

blueprint_authentication = Blueprint("authentication", __name__)


# Handles user registration and initiates 2FA setup.
@blueprint_authentication.route("/register", methods=["POST"])
@inject
def register(authentication_service: AuthenticationService):
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if not authentication_service.check_credentials(email, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate and send the initial code for 2FA setup
    try:
        secret = authentication_service.generate_2fa(email)
        response = {
            "message": "Registration successful, \
            scan the QR code in Google Authenticator",
            "secret": secret,
        }
        return response, 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Retrieves all user secrets from the database.
@blueprint_authentication.route("/user_secrets", methods=["GET"])
@inject
def get_all_user_secrets(authentication_service: AuthenticationService):
    try:
        user_secrets = authentication_service.get_all_user_secrets()
        return jsonify(user_secrets), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Verifies the 2FA code provided by the user and generates a JWT token upon
# successful verification.
@blueprint_authentication.route("/verify-2fa", methods=["POST"])
@inject
def verify(authentication_service: AuthenticationService):
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
                "your_secret_key",  # Replace this with your secret key
                algorithm="HS256",
            )
            return (
                jsonify({"message": "2FA verification successful", "token": token}),
                200,
            )
        else:
            return jsonify({"error": "Invalid 2FA code"}), 400
    except ValueError as e:
        error_message = str(e)
        if "No user found" in error_message:
            return jsonify({"error": error_message}), 404
        elif "No secrets found" in error_message:
            return jsonify({"error": error_message}), 404
        elif "wait before trying again" in error_message:
            return jsonify({"error": error_message}), 429
        else:
            return jsonify({"error": error_message}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
