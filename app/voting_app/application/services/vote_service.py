"""
Module: vote_service.py

Description: This module defines the `VoteService` class responsible for handling
vote-related operations  such as casting a vote, retrieving all votes, and fetching
votes by user. It interacts with both the `UserRepository` and `VoteRepository` to
manage voting data and ensures users and vote options are valid before allowing a
vote to be cast. The class also handles various exceptions for scenarios like user
not found, vote option not found, or if a user has already voted.

Classes:
    - VoteService: Provides methods for voting in an election, retrieving all votes,
        and fetching a user's vote.

Methods:
    - vote_in_election(user_id, vote_option_id): Allows a user to vote if they haven't
        voted yet and the vote option is valid.
    - get_all_votes(): Retrieves all votes from the repository.
    - get_vote(user_id): Fetches the vote of a specific user by their ID.

Dependencies:
    - UserRepository, VoteRepository: Repositories to interact with user and vote
        data stored in the database.
    - load_election: Utility function to load the current election data.
    - VoteNotFoundError, UserNotFoundError, VoteOptionNotFoundError,
        UserHasAlreadyVotedError: Custom exceptions
      to handle errors related to voting and user data.
"""

from ..repositories.user_repository import UserRepository
from ..repositories.vote_repository import VoteRepository
from ..utils.data_loader import load_election
from ..exceptions.error_classes import (
    VoteNotFoundError,
    UserNotFoundError,
    VoteOptionNotFoundError,
    UserHasAlreadyVotedError,
)


class VoteService:
    """
    Service class responsible for handling vote-related operations in an election.
    This includes managing user votes and interacting with the election data.
    """

    def __init__(
        self, user_repository: UserRepository, vote_repository: VoteRepository
    ):
        """
        Initializes the `VoteService` with `UserRepository` and `VoteRepository`
        instances.

        :param user_repository: An instance of `UserRepository` to
            manage user-related data.
        :param vote_repository: An instance of `VoteRepository` to
            manage vote-related data.
        """
        self.user_repository = user_repository
        self.vote_repository = vote_repository

    def vote_in_election(self, user_id, vote_option_id):
        """
        Cast a vote for the current election if the user hasn't already voted and the
        vote option is valid.

        :param user_id: The unique identifier of the user casting the vote.
        :param vote_option_id: The unique identifier of the vote option being selected.
        :raises UserNotFoundError: If the user does not exist.
        :raises VoteOptionNotFoundError: If the selected vote option does not exist.
        :raises UserHasAlreadyVotedError: If the user has already cast a vote.
        """
        # Retrieve the user and any existing vote for the given user_id
        user = self.user_repository.get_user(user_id)
        vote = self.vote_repository.get_vote_by_voter_id(user_id)

        # Load the available vote options for the current election
        vote_options = load_election().to_json()["vote_options"]

        # Check if the user exists in the system
        if not user:
            raise UserNotFoundError(user_id)

        # Verify that the selected vote option is valid
        if not any(
            vote_option.get("vote_option_id") == vote_option_id
            for vote_option in vote_options
        ):
            raise VoteOptionNotFoundError(vote_option_id)

        # Check if the user has already voted
        if vote:
            raise UserHasAlreadyVotedError(user_id)

        # Store the vote in the vote repository
        vote = {"user_id": user_id, "vote_option_id": vote_option_id}
        self.vote_repository.store_vote(vote)

    def get_all_votes(self):
        """
        Retrieves all votes stored in the repository.

        :return: A list of all votes.
        """
        return self.vote_repository.get_all_votes()

    def get_vote(self, user_id):
        """
        Fetches the vote of a specific user by their `user_id`.

        :param user_id: The unique identifier of the user whose vote is being retrieved.
        :return: The vote details as a dictionary.
        :raises VoteNotFoundError: If no vote is found for the user.
        """
        # Retrieve the user's vote from the repository
        vote = self.vote_repository.get_vote_by_voter_id(user_id)

        # Raise an error if the user has not voted
        if not vote:
            raise VoteNotFoundError(user_id)

        return vote
