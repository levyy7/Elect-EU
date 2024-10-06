from ..services.user_service import UserService
from ..services.vote_service import VoteService


class AdminController:
    @staticmethod
    def get_all_votes():
        return VoteService.get_all_votes()

    @staticmethod
    def get_all_users():
        return UserService.get_all_users()
