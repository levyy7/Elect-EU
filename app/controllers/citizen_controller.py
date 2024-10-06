from flask import jsonify
from ..models import Citizen
from ..utils.data_loader import load_election
from ..services.user_service import UserService
from ..services.vote_service import VoteService


class CitizenController:
    @staticmethod
    def get_current_election():
        currentElection = load_election()

        return currentElection.to_json()

    @staticmethod
    def create_citizen(user_id):
        all_users = UserService.get_all_users()

        if any(user.get("user_id") == user_id for user in all_users):
            return jsonify({"error": "Already exists a user with that user_id"}), 400
        else:
            citizen = Citizen(user_id)
            UserService.store_user(citizen.to_json())
            return jsonify({"message": "Citizen created succesfully"}), 200

    @staticmethod
    def vote_in_election(user_id, vote_option_id):
        all_users = UserService.get_all_users()
        all_votes = VoteService.get_all_votes()
        vote_options = load_election().to_json()["vote_options"]

        if not any(user.get("user_id") == user_id for user in all_users):
            return jsonify({"error": "The specified user does not exist"}), 401
        elif not any(
            vote_option.get("vote_option_id") == vote_option_id
            for vote_option in vote_options
        ):
            return jsonify({"error": "The specified vote_option does not exist"}), 402
        elif any(vote.get("user_id") == user_id for vote in all_votes):
            return jsonify({"error": "The specified user has already voted"}), 403
        else:
            vote = {"user_id": user_id, "vote_option_id": vote_option_id}
            VoteService.store_vote(vote)
            return jsonify({"message": "Vote submitted succesfully"}), 201
