from cryptography.fernet import Fernet

class Vote:
    # You should securely store the encryption key and load it from a secure place.
    # For demonstration purposes, we're generating a key here.
    key = Fernet.generate_key()  # This should be stored securely
    cipher = Fernet(key)

    def __init__(self, user_id, vote_id):
        self.user_id = user_id
        self.vote_id = vote_id

    def encrypt_data(self, data):
        # Encrypt the data
        encrypted_data = self.cipher.encrypt(data.encode('utf-8'))
        return encrypted_data.decode('utf-8')

    def to_json(self):
        # Encrypt user_id and vote_id before saving them
        return {
            "user_id": self.encrypt_data(self.user_id),
            "vote_id": self.encrypt_data(self.vote_id)
        }

    def decrypt_data(self, encrypted_data):
        # Decrypt the data
        decrypted_data = self.cipher.decrypt(encrypted_data.encode('utf-8'))
        return decrypted_data.decode('utf-8')

