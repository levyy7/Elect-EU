from injector import inject


class TokenRepository:
    @inject
    def __init__(self, mongo):
        self.mongo = mongo
        self.tokens_table = mongo.cx.votes_db.tokens
    
    def store_token(self, email, token):
        self.tokens_table.insert_one({"email": email, "token": token})

    def get_token(self, email):
        token = self.tokens_table.find_one({"email": email}, {"_id": 0})