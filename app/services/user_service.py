from ..models import Citizen, Admin
from ..repositories.user_repository import UserRepository
from ..exceptions.user_already_exists_error import UserAlreadyExistsError
from ..exceptions.user_not_found_error import UserNotFoundError


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_id, admin_rights=False):
        all_users = self.user_repository.get_all_users()

        if any(user.get("user_id") == user_id for user in all_users):
            raise UserAlreadyExistsError(user_id)

        if admin_rights:
            user = Admin(user_id)
        else:
            user = Citizen(user_id)
        self.user_repository.store_user(user.to_json())

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def get_user(self, user_id):
        user = self.user_repository.get_user(user_id)

        if not user:
            raise UserNotFoundError(user_id)

        return user

    def delete_user(self, user_id):
        result = self.user_repository.delete_user(user_id)

        if result == 0:
            raise UserNotFoundError(user_id)
