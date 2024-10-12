from injector import inject


class VoteRepository:
    @inject
    def __init__(self, mongo):
        self.mongo = mongo
        self.votes_table = mongo.cx.votes_db.votes

    def store_vote(self, vote_json):
        self.votes_table.insert_one(vote_json)

    def get_all_votes(self):
        return list(self.votes_table.find({}, {"_id": 0}))

    def get_vote_by_voter_id(self, user_id):
        vote = self.votes_table.find_one({"user_id": user_id}, {"_id": 0})

        return vote

    def delete_vote(self, user_id):
        result = self.votes_table.delete_one({"user_id": user_id})

        return result
