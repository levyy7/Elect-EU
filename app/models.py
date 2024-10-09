import bcrypt 

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_json(self):
        return {"username": self.username}


class Vote:
    def __init__(self, user_id, vote_id):
        self.user_id = user_id
        self.vote_id = vote_id

    def to_json(self):
        return {"user_id": self.user_id, "vote_id": self.vote_id}
