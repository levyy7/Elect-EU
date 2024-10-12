import pyotp
import qrcode
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from repositories.user_repository import save_secret_for_user, get_user_by_email

def send_email_with_qr_code(email, qr_code_path):
    # Email credentials
    sender_email = 'electeu@gmail.com'
    sender_password = 'kxvz hrel fgii qhdo'  # Use App Password if 2FA is enabled

    # Create a multipart email message
    msg = MIMEMultipart()
    msg['Subject'] = 'Your 2FA Setup QR Code'
    msg['From'] = sender_email
    msg['To'] = email

    # Add text to the email
    text = f'Scan the attached QR code to set up 2FA for {email}'
    msg.attach(MIMEText(text, 'plain'))

    # Read the QR code image and attach it to the email
    with open(qr_code_path, 'rb') as f:
        img_data = f.read()
        img_mime = MIMEImage(img_data, name=os.path.basename(qr_code_path))
        msg.attach(img_mime)

    # Send email using SMTP (ensure the SMTP server is correctly configured)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            print(f"Email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Generate 2FA secret and QR code
def generate_2fa(email):
    # Ensure the data directory exists
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Generate a unique secret for the user
    secret = pyotp.random_base32()
    save_secret_for_user(email, secret)

    # Generate a QR code for Google Authenticator
    totp = pyotp.TOTP(secret)
    qr_code_data = totp.provisioning_uri(email, issuer_name="ElectEU")
    img = qrcode.make(qr_code_data)

    # Save the QR code as an image
    qr_code_path = f'{data_dir}/{email}_qrcode.png'
    img.save(qr_code_path)

    # Send the QR code via email
    send_email_with_qr_code(email, qr_code_path)
    
    # Remove the QR code file after sending the email
    remove_qr_code = False  # Set to True to remove the QR code file after sending the email
    if remove_qr_code:
        try:
            os.remove(qr_code_path)
            print(f"Successfully deleted QR code file: {qr_code_path}")
        except Exception as e:
            print(f"Failed to delete QR code file: {e}")

    return secret

def verify_2fa(email, code):
    user = get_user_by_email(email)
    if not user:
        raise Exception("User not found")

    secret = user.get('2fa_secret')
    if secret is None:
        raise Exception("2FA secret not found for this user.")

    totp = pyotp.TOTP(secret)
    return totp.verify(code)

