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

    def get_vote_by_voter_id(self, bsn):
        vote = self.votes_table.find_one({"BSN": bsn}, {"_id": 0})

        return vote

    def delete_vote(self, bsn):
        result = self.votes_table.delete_one({"BSN": bsn})

        return result
