"""
Module: authentication_service.py
Description: This module provides the AuthenticationService class, responsible for handling user authentication,
two-factor authentication (2FA) setup, and email functionality for the ElectEU application.

Classes:
1. AuthenticationService: Handles user authentication operations such as generating 2FA secrets, sending emails with
   QR codes, verifying 2FA codes, and checking user credentials.
"""

import os
import pyotp
import qrcode
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from flask import jsonify
from ..repositories.authentication_repository import AuthenticationRepository


class AuthenticationService:
    """
    Service class for handling user authentication, including two-factor authentication (2FA) and credential verification.

    Attributes:
        authentication_repository: An instance of AuthenticationRepository to interact with the database.
    """

    def __init__(self, authentication_repository: AuthenticationRepository):
        """
        Initializes the AuthenticationService with the provided AuthenticationRepository instance.

        Args:
            authentication_repository: A repository instance to handle database operations related to authentication.
        """
        self.authentication_repository = authentication_repository

    def send_email_with_qr_code(self, email, qr_code_path):
        """
        Sends an email with the 2FA setup QR code as an attachment.

        Args:
            email: The recipient's email address.
            qr_code_path: The file path to the QR code image to be sent.

        Raises:
            Exception: If email sending fails due to an SMTP error.
        """
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
        """
        Generates a 2FA secret for the user, stores it in the database, and sends the corresponding QR code via email.

        Args:
            email: The user's email address.

        Returns:
            secret: The generated 2FA secret for the user.
        """
        # Ensure the data directory exists
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)  # Create the directory if it doesn't exist

        # Generate a unique secret for the user
        secret = pyotp.random_base32()

        # Store the secret in the database
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

        # Remove the QR code file after sending the email (if needed)
        remove_qr_code = False  # Set to True if you want to delete the QR code after sending the email
        if remove_qr_code:
            try:
                os.remove(qr_code_path)
                print(f"Successfully deleted QR code file: {qr_code_path}")
            except Exception as e:
                print(f"Failed to delete QR code file: {e}")

        return secret

    def verify_2fa(self, email, code):
        """
        Verifies the provided 2FA code for the user.

        Args:
            email: The user's email address.
            code: The 2FA code to verify.

        Returns:
            A JSON response indicating whether the verification was successful or not.
        """
        # Fetch the user's stored 2FA secret
        user_secrets = self.authentication_repository.get_user_secrets(email)

        if not user_secrets:
            return jsonify({"error": "User not found"}), 404

        # Get the authentication token (2FA secret) from the database
        authentication_token = user_secrets.get("authentication_token")
        if authentication_token is None:
            return (
                jsonify({"error": "Authentication token not found for this user."}),
                400,
            )

        # Verify the provided 2FA code
        totp = pyotp.TOTP(authentication_token)
        if totp.verify(code):
            return jsonify({"message": "2FA verification successful"}), 200
        else:
            return jsonify({"error": "Invalid 2FA code"}), 400

    def check_credentials(self, email, password):
        """
        Checks the user's credentials against the database.

        Args:
            email: The user's email address.
            password: The user's password.

        Returns:
            A boolean indicating whether the credentials are valid.
        """
        result = self.authentication_repository.verify(email, password)
        return result != 0

    def get_all_user_secrets(self):
        """
        Retrieves all stored user secrets from the database.

        Returns:
            A list of user secrets.
        """
        return self.authentication_repository.get_all_user_secrets()
