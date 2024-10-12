from flask import Blueprint, request, jsonify
from services.auth_service import generate_2fa, verify_2fa

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Generate and send the initial code for 2FA setup
    try:
        secret = generate_2fa(email)
        return jsonify({'message': 'Registration successful, \
                                    scan the QR code in Google Authenticator', 'secret': secret}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_blueprint.route('/verify-2fa', methods=['POST'])
def verify():
    email = request.json.get('email')
    code = request.json.get('code')
    
    if not email or not code:
        return jsonify({'error': 'Email and 2FA code are required'}), 400

    # Verify the 2FA code
    try:
        is_valid = verify_2fa(email, code)
        if is_valid:
            return jsonify({'message': '2FA verification successful'}), 200
        else:
            return jsonify({'error': 'Invalid 2FA code'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
