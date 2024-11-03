"""
Description: This file provides the AuthenticationService class,
and has the following functionalities:
- User authentication.
- Two-factor authentication (2FA) setup.
- Retrieving the complete user database.
- Verifying usrs
- Checking user credentials.
"""

import pyotp
import qrcode
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from flask import jsonify
from ..repositories.authentication_repository import AuthenticationRepository


class AuthenticationService:
    def __init__(self, authentication_repository: AuthenticationRepository):
        self.authentication_repository = authentication_repository

    def send_email_with_qr_code(self, email, qr_code_path):
        # Email credentials
        sender_email = "electeu@gmail.com"
        sender_password = "kxvz hrel fgii qhdo"  # Use App Password if 2FA is enabled

        # Create a multipart email message
        msg = MIMEMultipart()
        msg["Subject"] = "Your 2FA Setup QR Code"
        msg["From"] = sender_email
        msg["To"] = email

        # Add text to the email
        text = f"Scan the attached QR code to set up 2FA for {email}"
        msg.attach(MIMEText(text, "plain"))

        # Read the QR code image and attach it to the email
        with open(qr_code_path, "rb") as f:
            img_data = f.read()
            img_mime = MIMEImage(img_data, name=os.path.basename(qr_code_path))
            msg.attach(img_mime)

        # Send email using SMTP (ensure the SMTP server is correctly configured)
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, msg.as_string())
                print(f"Email sent to {email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def generate_2fa(self, email):
        # Ensure the data directory exists
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)  # Create the directory if it doesn't exist

        # Generate a unique secret for the user
        secret = pyotp.random_base32()

        # token_service.store_token(email, secret)
        self.authentication_repository.store_totp_secret(email, secret)

        # Generate a QR code for Google Authenticator
        totp = pyotp.TOTP(secret)
        qr_code_data = totp.provisioning_uri(email, issuer_name="ElectEU")
        img = qrcode.make(qr_code_data)

        # Save the QR code as an image
        qr_code_path = f"{data_dir}/{email}_qrcode.png"
        img.save(qr_code_path)

        # Send the QR code via email
        self.send_email_with_qr_code(email, qr_code_path)

        # Remove the QR code file after sending the email
        remove_qr_code = False
        if remove_qr_code:
            try:
                os.remove(qr_code_path)
                print(f"Successfully deleted QR code file: {qr_code_path}")
            except Exception as e:
                print(f"Failed to delete QR code file: {e}")

        return secret

    def verify_2fa(self, email, code):
        # Search for the user in the 'users' collection by email
        # user = token_service.get_token(email)
        user_secrets = self.authentication_repository.get_user_secrets(email)

        if not user_secrets:
            return jsonify({"error": "User not found"}), 404

        # Access the authentication token from the user's record
        authentication_token = user_secrets.get("authentication_token")
        if authentication_token is None:
            return (
                jsonify({"error": "Authentication token not found for this user."}),
                400,
            )

        # Use the authentication token to verify the 2FA code
        totp = pyotp.TOTP(authentication_token)
        if totp.verify(code):
            return jsonify({"message": "2FA verification successful"}), 200
        else:
            return jsonify({"error": "Invalid 2FA code"}), 400

    def check_credentials(self, email, password):
        result = self.authentication_repository.verify(email, password)
        if result == 0:
            return False
        else:
            return True

    def get_all_user_secrets(self):
        """Retrieve all user secrets."""
        return self.authentication_repository.get_all_user_secrets()
