from flask import request, jsonify, Blueprint
from flask_injector import inject
from ..services.user_service import UserService
from ..services.vote_service import VoteService
from ..services.election_service import ElectionService
from ..exceptions.user_not_found_error import UserNotFoundError
from ..exceptions.vote_option_not_found_error import VoteOptionNotFoundError
from ..exceptions.user_has_already_voted_error import UserHasAlreadyVotedError
from ..exceptions.user_already_exists_error import UserAlreadyExistsError
from ..exceptions.missing_fields_error import MissingFieldsError

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

        if not data.get("BSN") or not data.get("password"):
            raise MissingFieldsError()

        user_service.create_user(data)

        return jsonify({"message": "Citizen created succesfully"}), 200
    except MissingFieldsError as e:
        return jsonify({"error": str(e)}), 400
    except UserAlreadyExistsError as e:
        return jsonify({"error": str(e)}), 402
    except Exception as e:
        msg = "Internal Server Error: " + str(e)
        return jsonify({"error": msg}), 500


@blueprint_citizen.route("/vote", methods=["POST"])
@inject
def vote(vote_service: VoteService):
    try:
        data = request.get_json()
        bsn, vote_option_id = data.get("BSN"), data.get("vote_option_id")

        if not bsn or not vote_option_id:
            raise MissingFieldsError()

        vote_service.vote_in_election(bsn, vote_option_id)

        return jsonify({"message": "Vote submitted succesfully."}), 200
    except MissingFieldsError as e:
        return jsonify({"error": str(e)}), 400
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except VoteOptionNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except UserHasAlreadyVotedError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        msg = "Internal Server Error: " + str(e)
        return jsonify({"error": msg}), 500

