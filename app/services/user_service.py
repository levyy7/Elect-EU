# from flask import jsonify
from ..models import Citizen, Admin
from ..repositories.user_repository import UserRepository
from ..exceptions.user_already_exists_error import UserAlreadyExistsError
from ..exceptions.user_not_found_error import UserNotFoundError


class UserService:

    @staticmethod
    def create_user(user_id, admin_rights=False):
        all_users = UserRepository.get_all_users()

        if any(user.get("user_id") == user_id for user in all_users):
            raise UserAlreadyExistsError(user_id)

        if admin_rights:
            user = Admin(user_id)
        else:
            user = Citizen(user_id)
        UserRepository.store_user(user.to_json())

    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()

    @staticmethod
    def get_user(user_id):
        user = UserRepository.get_user(user_id)

        if not user:
            raise UserNotFoundError(user_id)

        return user

    @staticmethod
    def delete_user(user_id):
        result = UserRepository.delete_user(user_id)

        if result == 0:
            raise UserNotFoundError(user_id)
