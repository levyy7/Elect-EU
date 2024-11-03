"""
Description: Exception raised when the user does not exist in the databse.
"""


class UserNotFoundError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
        self.message = f"User with id {user_id} not found."
        super().__init__(self.message)

    def __str__(self):
        return f"UserNotFoundError: {self.message}"
