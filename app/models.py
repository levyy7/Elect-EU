from cryptography.fernet import Fernet


class Vote:
    # This is a specific type of symmetric encryption
    # provided by the cryptography library.
    # It uses AES in CBC mode with a SHA256 HMAC for authentication.
    # Fernet ensures that the data is both encrypted and verified.
    # This should be stored securely, we can use environment variables or
    # for gitlab configuration files
    # The best case is to use key faults like Azure or AWS or HashiCorp.
    # Azure also uses Hardware Security modules to safely store you secrets.
    # This is outside of the scope (too many man hours to correctly implement this)
    key = Fernet.generate_key()
    cipher = Fernet(key)

    def __init__(self, user_id, vote_id):
        self.user_id = user_id
        self.vote_id = vote_id

    def encrypt_data(self, data):
        # Encrypt the data
        encrypted_data = self.cipher.encrypt(data.encode("utf-8"))
        return encrypted_data.decode("utf-8")

    def to_json(self):
        # Encrypt user_id and vote_id before saving them
        return {
            "user_id": self.encrypt_data(self.user_id),
            "vote_id": self.encrypt_data(self.vote_id),
        }

    def decrypt_data(self, encrypted_data):
        # Decrypt the data
        decrypted_data = self.cipher.decrypt(encrypted_data.encode("utf-8"))
        return decrypted_data.decode("utf-8")
