from flask import request, jsonify
from app import app
from app.services import VoteService
from app.models import Vote


@app.route("/vote", methods=["POST"])
def store_vote():
    data = request.get_json()
    user_id = data.get("user_id")
    vote_id = data.get("vote_id")

    if not user_id or not vote_id:
        return jsonify({"error": "Missing fields"}), 400

    vote = Vote(user_id, vote_id)
    VoteService.store_vote(vote)
    return jsonify({"message": "Vote stored successfully"}), 201


@app.route("/votes", methods=["GET"])
def get_votes():
    votes = VoteService.get_all_votes()
    return jsonify(votes), 200
