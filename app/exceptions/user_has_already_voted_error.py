class UserHasAlreadyVotedError(Exception):

    def __init__(self, user_id):
        self.user_id = user_id
        self.message = (
            f"User with id {user_id} has already voted in the current election."
        )
        super().__init__(self.message)

    def __str__(self):
        return f"UserAlreadyExistsError: {self.message}"
