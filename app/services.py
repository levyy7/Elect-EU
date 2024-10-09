from app import mongo
from app.models import Vote


class VoteService:
    @staticmethod
    def store_vote(vote: Vote):
        mongo.db.votes.insert_one(vote.encrypt_json())

    @staticmethod
    def get_all_votes_raw():
        return list(mongo.db.votes.find({}, {"_id": 0}))

    @staticmethod
    def get_all_votes():
        # Retrieve all votes from the database
        encrypted_votes = list(mongo.db.votes.find({}, {"_id": 0}))

        # Decrypt each vote
        decrypted_votes = []
        for vote_data in encrypted_votes:
            vote = Vote("", "")  # Create a Vote object
            decrypted_vote = {
                "user_id": vote.decrypt_data(vote_data["user_id"]),
                "vote_id": vote.decrypt_data(vote_data["vote_id"]),
            }
            decrypted_votes.append(decrypted_vote)

        return decrypted_votes
