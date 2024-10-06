from flask import request, jsonify
from app import app
from app.controllers.citizen_controller import CitizenController
from app.controllers.admin_controller import AdminController


@app.route("/election", methods=["GET"])
def get_election():
    election = CitizenController.get_current_election()
    return jsonify(election), 200


@app.route("/register", methods=["POST"])
def register_citizen():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing fields"}), 400

    return CitizenController.create_citizen(user_id)


@app.route("/users", methods=["GET"])
def get_users():
    users = AdminController.get_all_users()
    return jsonify(users), 200


@app.route("/vote", methods=["POST"])
def store_vote():
    data = request.get_json()
    user_id = data.get("user_id")
    vote_option_id = data.get("vote_option_id")

    if not user_id or not vote_option_id:
        return jsonify({"error": "Missing fields"}), 400

    return CitizenController.vote_in_election(user_id, vote_option_id)


@app.route("/votes", methods=["GET"])
def get_votes():
    votes = AdminController.get_all_votes()
    return jsonify(votes), 200
