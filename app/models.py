import bcrypt

class Vote:
    def __init__(self, user_id, vote_id):
        self.user_id = user_id
        self.vote_id = vote_id

    def hash_data(self, data):
        # Bcrypt automatically handles salting
        salt = bcrypt.gensalt()
        hashed_data = bcrypt.hashpw(data.encode('utf-8'), salt)
        return hashed_data.decode('utf-8')

    def to_json(self):
        # Hash user_id and vote_id before saving them
        return {
            "user_id": self.hash_data(self.user_id),
            "vote_id": self.hash_data(self.vote_id)
        }
