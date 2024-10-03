from app import mongo
from app.models import Vote

class VoteService:
    @staticmethod
    def store_vote(vote: Vote):
        mongo.db.votes.insert_one(vote.to_json())

    @staticmethod
    def get_all_votes():
        return list(mongo.db.votes.find({}, {"_id": 0}))
