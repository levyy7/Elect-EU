from app import mongo


class VoteRepository:
    @staticmethod
    def store_vote(vote_json):
        mongo.db.votes.insert_one(vote_json)

    @staticmethod
    def get_all_votes():
        return list(mongo.db.votes.find({}, {"_id": 0}))

    @staticmethod
    def get_vote(user_id):
        vote = mongo.db.votes.find_one({"user_id": user_id}, {"_id": 0})

        return vote

    @staticmethod
    def delete_vote(user_id):
        result = mongo.db.votes.delete_one({"user_id": user_id})

        return result
