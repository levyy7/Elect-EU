from flask import request, jsonify
from app import app
from ..services.user_service import UserService
from ..services.vote_service import VoteService
from ..exceptions.user_not_found_error import UserNotFoundError
from ..exceptions.missing_fields_error import MissingFieldsError


class AdminController:
    @app.route("/users", methods=["GET"])
    def get_users():
        try:
            return UserService.get_all_users()
        except Exception:
            return jsonify({"error": "Internal Server Error"}), 500
        
    @app.route("/user_delete", methods=["POST"])
    def delete_user():
        try:
            data = request.get_json()
            user_id = data.get("user_id")

            if not user_id:
                raise MissingFieldsError()

            UserService.delete_user(user_id)
            
            return jsonify({"message": "User deleted succesfully"}), 200
        except MissingFieldsError as e:
            return jsonify({"error": str(e)}), 400
        except UserNotFoundError as e:
            return jsonify({"error": str(e)}), 402
        except Exception:
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route("/votes", methods=["GET"])
    def get_votes():
        try:
            return VoteService.get_all_votes()
        except Exception:
            return jsonify({"error": "Internal Server Error"}), 500
