from ..repositories.user_repository import UserRepository
from ..repositories.vote_repository import VoteRepository
from ..utils.data_loader import load_election
from ..exceptions.vote_not_found_error import VoteNotFoundError
from ..exceptions.user_not_found_error import UserNotFoundError
from ..exceptions.vote_option_not_found_error import VoteOptionNotFoundError
from ..exceptions.user_has_already_voted_error import UserHasAlreadyVotedError


class VoteService:
    @staticmethod
    def vote_in_election(user_id, vote_option_id):
        user = UserRepository.get_user(user_id)
        vote = VoteRepository.get_vote(user_id)
        vote_options = load_election().to_json()["vote_options"]

        if not user:
            raise UserNotFoundError(user_id)
        if not any(
            vote_option.get("vote_option_id") == vote_option_id
            for vote_option in vote_options
        ):
            raise VoteOptionNotFoundError(vote_option_id)
        if vote:
            raise UserHasAlreadyVotedError(user_id)
        
        vote = {"user_id": user_id, "vote_option_id": vote_option_id}
        VoteService.store_vote(vote)
        
    @staticmethod
    def get_all_votes():
        return VoteRepository.get_all_votes()

    @staticmethod
    def get_vote(user_id):
        vote = VoteRepository.get_vote(user_id)

        if not vote:
            raise VoteNotFoundError(user_id)

        return vote
