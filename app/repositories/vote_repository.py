from injector import inject


class VoteRepository:
    @inject
    def __init__(self, mongo):
        self.mongo = mongo

    def store_vote(self, vote_json):
        self.mongo.db.votes.insert_one(vote_json)

    def get_all_votes(self):
        return list(self.mongo.db.votes.find({}, {"_id": 0}))

    def get_vote(self, user_id):
        vote = self.mongo.db.votes.find_one({"user_id": user_id}, {"_id": 0})

        return vote

    def delete_vote(self, user_id):
        result = self.mongo.db.votes.delete_one({"user_id": user_id})

        return result
