import unittest
import pyotp
from services.auth_service import generate_2fa, verify_2fa


class TestAuthService(unittest.TestCase):
    def test_generate_2fa(self):
        email = "test@example.com"
        secret = generate_2fa(email)
        self.assertIsNotNone(secret)

    def test_verify_2fa(self):
        email = "test@example.com"
        secret = generate_2fa(email)
        self.assertTrue(verify_2fa(email, pyotp.TOTP(secret).now()))


if __name__ == "__main__":
    unittest.main()
