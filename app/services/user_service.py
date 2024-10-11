from ..models import Citizen, Admin
from ..repositories.user_repository import UserRepository
from ..exceptions.user_already_exists_error import UserAlreadyExistsError
from ..exceptions.user_not_found_error import UserNotFoundError


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, data, admin_rights=False):
        all_users = self.user_repository.get_all_users()
        email, password, bsn = data.get("email"), data.get("password"), data.get("BSN")

        if any(user.get("BSN") == bsn for user in all_users):
            raise UserAlreadyExistsError(bsn)

        if admin_rights:
            user = Admin(email, password, bsn)
        else:
            user = Citizen(email, password, bsn)
        self.user_repository.store_user(user.to_json())

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def get_user(self, bsn):
        user = self.user_repository.get_user(bsn)

        if not user:
            raise UserNotFoundError(bsn)

        return user

    def delete_user(self, bsn):
        result = self.user_repository.delete_user(bsn)

        if result == 0:
            raise UserNotFoundError(bsn)
