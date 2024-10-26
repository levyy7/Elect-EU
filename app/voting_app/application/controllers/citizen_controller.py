from flask import request, jsonify, Blueprint
from flask_injector import inject
from ..services.user_service import UserService
from ..services.vote_service import VoteService
from ..services.election_service import ElectionService
from ..exceptions.user_already_exists_error import UserAlreadyExistsError
from ..exceptions.missing_fields_error import MissingFieldsError
import jwt

blueprint_citizen = Blueprint("citizen", __name__)


@blueprint_citizen.route("/election", methods=["GET"])
@inject
def get_election(election_service: ElectionService):
    try:
        election = election_service.get_current_election()
        return (jsonify(election), 200)
    except Exception as e:
        msg = "Internal Server Error: " + str(e)
        return jsonify({"error": msg}), 500


@blueprint_citizen.route("/register", methods=["POST"])
@inject
def register_citizen(user_service: UserService):
    try:
        data = request.get_json()

        if not data.get("user_id") or not data.get("password") or not data.get("email"):
            raise MissingFieldsError()

        user_service.create_user(data)

        return jsonify({"message": "Citizen created succesfully"}), 200
    except MissingFieldsError as e:
        return jsonify({"error": str(e)}), 400
    except UserAlreadyExistsError as e:
        return jsonify({"error": str(e)}), 402
    except Exception as e:
        msg = "Internal Server Error: " + str(e)
        print(msg)  # Log the error message
        return jsonify({"error": msg}), 500


@blueprint_citizen.route("/vote", methods=["POST"])
@inject
def vote(vote_service: VoteService):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization token is missing or invalid"}), 401

    token = auth_header.split(" ")[1]

    try:
        # Verify the token
        decoded_token = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        user_id = decoded_token["user_id"]

        data = request.get_json()
        vote_option_id = data.get("vote_option_id")

        if not user_id or not vote_option_id:
            raise MissingFieldsError()

        vote_service.vote_in_election(user_id, vote_option_id)

        return jsonify({"message": "Vote submitted successfully."}), 200
    except MissingFieldsError as e:
        return jsonify({"error": str(e)}), 400
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
