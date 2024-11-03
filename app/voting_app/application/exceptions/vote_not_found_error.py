"""
Description: Exception raised when the user has not voted in the current election.
"""


class VoteNotFoundError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
        self.message = (
            f"The user with id {user_id} has not voted in the current election."
        )
        super().__init__(self.message)

    def __str__(self):
        return f"VoteNotFoundError: {self.message}"
