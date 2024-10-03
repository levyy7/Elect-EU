class Vote:
    def __init__(self, user_id, vote_id):
        self.user_id = user_id
        self.vote_id = vote_id

    def to_json(self):
        return {
            "user_id": self.user_id,
            "vote_id": self.vote_id
        }
