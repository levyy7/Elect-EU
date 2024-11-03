"""
Description: Exception raised when you try to add a user that already
    exists in the database.
"""


class UserAlreadyExistsError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
        self.message = f"User with id {user_id} already exists."
        super().__init__(self.message)

    def __str__(self):
        return f"UserAlreadyExistsError: {self.message}"
