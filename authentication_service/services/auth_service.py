import pyotp
import qrcode
import os
import smtplib
from email.mime.text import MIMEText
from repositories.user_repository import get_user_by_email, save_secret_for_user

# Generate 2FA secret and QR code
def generate_2fa(email):
    user = get_user_by_email(email)
    if not user:
        raise Exception("User not found")
    
    # Generate a unique secret for the user
    secret = pyotp.random_base32()

    # Save the secret to the database (or repository)
    save_secret_for_user(email, secret)

    # Generate a QR code for Google Authenticator
    totp = pyotp.TOTP(secret)
    qr_code_data = totp.provisioning_uri(email, issuer_name="ElectEU")
    img = qrcode.make(qr_code_data)

    # Save the QR code as an image (this can be sent to the user via email)
    qr_code_path = f'./data/{email}_qrcode.png'
    img.save(qr_code_path)

    # Optionally, send the QR code via email (simplified here)
    send_email_with_qr_code(email, qr_code_path)

    return secret

def verify_2fa(email, code):
    user = get_user_by_email(email)
    if not user:
        raise Exception("User not found")
    
    secret = user['2fa_secret']
    totp = pyotp.TOTP(secret)
    return totp.verify(code)

def send_email_with_qr_code(email, qr_code_path):
    # Simulate sending email with the QR code (simplified)
    msg = MIMEText(f'Scan the attached QR code to set up 2FA for {email}')
    msg['Subject'] = 'Your 2FA Setup QR Code'
    msg['From'] = 'noreply@electeu.com'
    msg['To'] = email

    # Attach QR code image (omitted for simplicity)
    # Send email using SMTP (e.g., Gmail SMTP or local SMTP server)
    with smtplib.SMTP('localhost') as server:
        server.sendmail('noreply@electeu.com', email, msg.as_string())
