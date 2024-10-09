from flask import request, jsonify, Blueprint
from flask_injector import inject
from ..services.user_service import UserService
from ..services.vote_service import VoteService
from ..exceptions.user_not_found_error import UserNotFoundError
from ..exceptions.missing_fields_error import MissingFieldsError

blueprint_admin = Blueprint("admin", __name__)


@blueprint_admin.route("/users", methods=["GET"])
@inject
def get_users(user_service: UserService):
    try:
        return jsonify(user_service.get_all_users()), 200
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500


@blueprint_admin.route("/user_delete", methods=["POST"])
@inject
def delete_user(user_service: UserService):
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        if not user_id:
            raise MissingFieldsError()

        user_service.delete_user(user_id)

        return jsonify({"message": "User deleted succesfully."}), 200
    except MissingFieldsError as e:
        return jsonify({"error": str(e)}), 400
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 402
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500


@blueprint_admin.route("/votes", methods=["GET"])
@inject
def get_votes(vote_service: VoteService):
    try:
        return jsonify(vote_service.get_all_votes()), 200
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
