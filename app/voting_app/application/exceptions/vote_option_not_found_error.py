"""
Description: Exception raised when the user tries to vote on a option
that does not exist for that election.
"""


class VoteOptionNotFoundError(Exception):
    def __init__(self, vote_option_id):
        self.vote_option_id = vote_option_id
        self.message = f"Vote option with id {vote_option_id} does not exist."
        super().__init__(self.message)

    def __str__(self):
        return f"VoteOptionNotFoundError: {self.message}"
