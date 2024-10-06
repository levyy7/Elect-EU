from app import mongo
from flask import jsonify


class VoteService:
    @staticmethod
    def store_vote(vote_json):
        mongo.db.votes.insert_one(vote_json)

    @staticmethod
    def get_all_votes():
        return list(mongo.db.votes.find({}, {"_id": 0}))

    @staticmethod
    def get_vote(user_id):
        vote = mongo.db.votes.find_one({"user_id": user_id}, {"_id": 0})

        if vote:
            return jsonify(vote)
        else:
            return jsonify({"error": "User not found"}), 404
