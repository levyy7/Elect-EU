from flask import Blueprint, request, jsonify
from services.auth_service import generate_2fa, verify_2fa
import sys
sys.path.append("..")
from ...authentication_service import db

auth_blueprint = Blueprint("auth", __name__)

def check_user_credentials(email, password):
    # Search for the user in the 'users' collection by email
    user = db.users.find_one({"email": email})
    return user and user["password"] == password

@auth_blueprint.route("/register", methods=["POST"])
def register():
    email = request.json.get("email")
    password = request.json.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if not check_user_credentials(email, password): 
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Generate and send the initial code for 2FA setup
    try:
        secret = generate_2fa(email)
        return (
            jsonify(
                {
                    "message": "Registration successful, \
                                    scan the QR code in Google \
                                    Authenticator",
                    "secret": secret,
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_blueprint.route("/verify-2fa", methods=["POST"])
def verify():
    email = request.json.get("email")
    code = request.json.get("code")

    if not email or not code:
        return jsonify({"error": "Email and 2FA code are required"}), 400

    # Verify the 2FA code
    try:
        is_valid = verify_2fa(email, code)
        if is_valid:
            return jsonify({"message": "2FA verification successful"}), 200
        else:
            return jsonify({"error": "Invalid 2FA code"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
