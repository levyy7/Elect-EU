"""
Module: admin_controller.py

Description: This module defines the routes for admin-related functionalities,
such as managing users and votes. It includes routes for fetching all users,
deleting a user, and retrieving all votes. Dependency injection is utilized
through Flask-Injector for service management, and custom exceptions are
handled to ensure appropriate error responses.

Routes:
    - GET /users: Fetch all users
    - DELETE /user: Delete a specific user by user_id
    - GET /votes: Fetch all votes

Dependencies:
    - UserService: For user management operations
    - VoteService: For vote management operations
"""

from flask import (
    request,
    jsonify,
    Blueprint,
)  # Import Flask modules for request handling, JSON response, and Blueprint
from flask_injector import inject  # Import Flask-Injector for dependency injection
from ..services.user_service import (
    UserService,
)  # Import the UserService for handling user-related logic
from ..services.vote_service import (
    VoteService,
)  # Import the VoteService for handling vote-related logic
from ..exceptions.error_classes import (
    UserNotFoundError,
    MissingFieldsError,
)  # Import custom error classes

# Define a Blueprint for admin-related routes
blueprint_admin = Blueprint("admin", __name__)


# Route for getting all users
@blueprint_admin.route("/users", methods=["GET"])
@inject  # Flask-Injector is used to inject the UserService dependency
def get_users(user_service: UserService):
    """
    Retrieves all users from the UserService.

    :param user_service: Injected instance of UserService for fetching users
    :return: JSON response containing the list of users or an error message
    """
    try:
        return (
            jsonify(user_service.get_all_users()),
            200,
        )  # Return the list of users with status code 200
    except Exception as e:
        # Handle any server-side errors and return a 500 Internal Server Error
        msg = "Internal Server Error: " + str(e)
        return jsonify({"error": msg}), 500


# Route for deleting a user
@blueprint_admin.route("/user", methods=["DELETE"])
@inject  # Flask-Injector is used to inject the UserService dependency
def delete_user(user_service: UserService):
    """
    Deletes a user based on the provided user_id.

    :param user_service: Injected instance of UserService for deleting a user
    :return: JSON response indicating success or failure of deletion
    """
    try:
        data = request.get_json()  # Get the JSON data from the request
        user_id = data.get("user_id")  # Extract the user_id from the JSON payload

        if not user_id:
            # Raise a custom error if the user_id is missing
            raise MissingFieldsError()

        # Attempt to delete the user by calling the UserService
        user_service.delete_user(user_id)

        return (
            jsonify({"message": "User deleted succesfully."}),
            200,
        )  # Success message if the user is deleted
    except MissingFieldsError as err:
        # Handles missing fields error (user_id not provided)
        # and return a 400 Bad Request
        return jsonify({"error": str(err)}), 400
    except UserNotFoundError as err:
        # Handles where the user is not found and return a 402 error (custom)
        return jsonify({"error": str(err)}), 402
    except Exception as err:
        # Handle any server-side errors and return a 500 Internal Server Error
        msg = "Internal Server Error: " + str(err)
        return jsonify({"error": msg}), 500


# Route for getting all votes
@blueprint_admin.route("/votes", methods=["GET"])
@inject  # Flask-Injector is used to inject the VoteService dependency
def get_votes(vote_service: VoteService):
    """
    Retrieves all votes from the VoteService.

    :param vote_service: Injected instance of VoteService for fetching votes
    :return: JSON response containing the list of votes or an error message
    """
    try:
        return (
            jsonify(vote_service.get_all_votes()),
            200,
        )  # Return the list of votes with status code 200
    except Exception as err:
        # Handle any server-side errors and return a 500 Internal Server Error
        msg = "Internal Server Error: " + str(err)
        return jsonify({"error": msg}), 500
