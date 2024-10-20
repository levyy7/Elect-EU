"""
Module: citizen_controller.py

Description: This module defines the routes for citizen-related functionalities
such as retrieving election data, registering as a citizen, and submitting a vote.
It includes routes for fetching the current election, registering a user, and
submitting votes with JWT-based authorization for vote submission. Flask-Injector
is used for dependency injection, and custom exceptions are handled for appropriate
error responses.

Routes:
    - GET /election: Get the current election details
    - POST /register: Register a new citizen
    - POST /vote: Submit a vote (JWT token required)

Dependencies:
    - UserService: For user management operations
    - VoteService: For vote management operations
    - ElectionService: For election management operations
"""

from flask import (
    request,
    jsonify,
    Blueprint,
)  # Import Flask modules for handling requests, JSON response, and Blueprint
from flask_injector import inject  # Import Flask-Injector for dependency injection
from ..services.user_service import (
    UserService,
)  # Import UserService for user-related operations
from ..services.vote_service import (
    VoteService,
)  # Import VoteService for vote-related operations
from ..services.election_service import (
    ElectionService,
)  # Import ElectionService for election-related operations
from ..exceptions.error_classes import (
    UserAlreadyExistsError,
    MissingFieldsError,
)  # Import custom error classes
import jwt  # Import JWT for token verification

# Define a Blueprint for citizen-related routes
blueprint_citizen = Blueprint("citizen", __name__)


# Route for getting the current election
@blueprint_citizen.route("/election", methods=["GET"])
@inject  # Flask-Injector is used to inject the ElectionService dependency
def get_election(election_service: ElectionService):
    """
    Retrieves the current election details from the ElectionService.

    :param election_service: Injected instance of ElectionService for
    fetching election data
    :return: JSON response containing election data or an error message
    """
    try:
        election = (
            election_service.get_current_election()
        )  # Fetch current election details
        return jsonify(election), 200  # Return election data with status code 200
    except Exception as e:
        # Handle any server-side errors and return a 500 Internal Server Error
        msg = "Internal Server Error: " + str(e)
        return jsonify({"error": msg}), 500


# Route for registering a new citizen
@blueprint_citizen.route("/register", methods=["POST"])
@inject  # Flask-Injector is used to inject the UserService dependency
def register_citizen(user_service: UserService):
    """
    Registers a new citizen by calling the UserService to create the user.

    :param user_service: Injected instance of UserService for creating the user
    :return: JSON response indicating success or failure of registration
    """
    try:
        data = request.get_json()  # Get the JSON data from the request

        # Check if both user_id and password are provided
        if not data.get("user_id") or not data.get("password"):
            raise MissingFieldsError()

        # Call UserService to create the user
        user_service.create_user(data)

        return (
            jsonify({"message": "Citizen created successfully"}),
            200,
        )  # Success message
    except MissingFieldsError as e:
        # Handle missing fields error (user_id or password not provided) and
        # return a 400 Bad Request
        return jsonify({"error": str(e)}), 400
    except UserAlreadyExistsError as e:
        # Handles where the user already exists and return a 402 error (custom)
        return jsonify({"error": str(e)}), 402
    except Exception as e:
        # Handle any server-side errors and return a 500 Internal Server Error
        msg = "Internal Server Error: " + str(e)
        return jsonify({"error": msg}), 500


# Route for submitting a vote (JWT token required)
@blueprint_citizen.route("/vote", methods=["POST"])
@inject  # Flask-Injector is used to inject the VoteService dependency
def vote(vote_service: VoteService):
    """
    Submits a vote for the current election, validating the JWT token from
    the Authorization header.

    :param vote_service: Injected instance of VoteService for handling
    the voting process
    :return: JSON response indicating success or failure of the vote submission
    """
    # Get the Authorization header containing the JWT token
    auth_header = request.headers.get("Authorization")

    # Validate that the token is present and correctly formatted
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization token is missing or invalid"}), 401

    # Extract the token from the header
    token = auth_header.split(" ")[1]

    try:
        # Verify the token using the secret key and the HS256 algorithm
        decoded_token = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        user_id = decoded_token["user_id"]  # Extract the user_id from the decoded token

        data = request.get_json()  # Get the JSON data from the request
        vote_option_id = data.get(
            "vote_option_id"
        )  # Extract the vote_option_id from the request

        # Check if both user_id and vote_option_id are provided
        if not user_id or not vote_option_id:
            raise MissingFieldsError()

        # Call VoteService to register the vote in the current election
        vote_service.vote_in_election(user_id, vote_option_id)

        return (
            jsonify({"message": "Vote submitted successfully."}),
            200,
        )  # Success message
    except jwt.ExpiredSignatureError:
        # Handles where the token has expired and return a 401 Unauthorized error
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        # Handles where the token is invalid and return a 401 Unauthorized error
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        # Handles any other errors and return a 500 Internal Server Error
        return jsonify({"error": str(e)}), 500
