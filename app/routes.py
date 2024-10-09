from flask import request, jsonify
from app import app
from app.services import VoteService, AuthService
from app.models import Vote, User
from functools import wraps  # Ensure this is imported

users = {
    "john_doe": User("john_doe", "password123")
}

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = users.get(username)

    if user and user.check_password(password):
        token = AuthService.create_token(user)
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

def token_required(f):
    @wraps(f)  # This ensures that Flask recognizes the original function
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({"error": "Token is missing"}), 403

        token = token.split(' ')[1]  # Get the actual token
        user_id = AuthService.verify_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 403

        return f(user_id, *args, **kwargs)  # Call the original function
    return decorated

@app.route("/vote", methods=["POST"])
def store_vote():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    vote_id = data.get("vote_id")

    # Check for necessary fields
    if not username or not password or not vote_id:
        return jsonify({"error": "Username, password, and vote_id are required"}), 400

    # Authenticate the user with username and password
    user = users.get(username)
    if user and user.check_password(password):
        # Create the vote if authentication is successful
        vote = Vote(username, vote_id)  # Store the vote using username or user ID
        VoteService.store_vote(vote)
        return jsonify({"message": "Vote stored successfully"}), 201
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/votes", methods=["GET"])
@token_required
def get_votes(user_id):
    votes = VoteService.get_all_votes()
    return jsonify(votes), 200
