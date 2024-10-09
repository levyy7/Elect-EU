from ..repositories.user_repository import UserRepository
from ..repositories.vote_repository import VoteRepository
from ..utils.data_loader import load_election
from ..exceptions.vote_not_found_error import VoteNotFoundError
from ..exceptions.user_not_found_error import UserNotFoundError
from ..exceptions.vote_option_not_found_error import VoteOptionNotFoundError
from ..exceptions.user_has_already_voted_error import UserHasAlreadyVotedError


class VoteService:
    def __init__(
        self, user_repository: UserRepository, vote_repository: VoteRepository
    ):
        self.user_repository = user_repository
        self.vote_repository = vote_repository

    def vote_in_election(self, user_id, vote_option_id):
        user = self.user_repository.get_user(user_id)
        vote = self.vote_repository.get_vote(user_id)
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
        self.vote_repository.store_vote(vote)

    def get_all_votes(self):
        return self.vote_repository.get_all_votes()

    def get_vote(self, user_id):
        vote = self.vote_repository.get_vote(user_id)

        if not vote:
            raise VoteNotFoundError(user_id)

        return vote
