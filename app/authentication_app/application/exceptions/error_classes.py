"""
Module Name: error_classes.py
Description: This module contains custom exception classes related to user authentication and voting functionality.

The exceptions are grouped into two categories:
1. User related exceptions: Handles cases like missing fields, user not found, and duplicate users.
2. Vote related exceptions: Handles errors related to the voting process, such as missing votes or invalid vote options.
"""

# User-related errors

class MissingFieldsError(Exception):
    """
    Exception raised when required fields are missing in a request or operation.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self):
        self.message = "Missing fields."
        super().__init__(self.message)

    def __str__(self):
        return f"MissingFieldsError: {self.message}"


class UserAlreadyExistsError(Exception):
    """
    Exception raised when an attempt is made to create a user that already exists.

    Attributes:
        user_id -- id of the user that caused the exception
        message -- explanation of the error
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.message = f"User with id {user_id} already exists."
        super().__init__(self.message)

    def __str__(self):
        return f"UserAlreadyExistsError: {self.message}"


class UserHasAlreadyVotedError(Exception):
    """
    Exception raised when a user attempts to vote more than once in the same election.

    Attributes:
        user_id -- id of the user that caused the exception
        message -- explanation of the error
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.message = f"User with id {user_id} has already voted in the current election."
        super().__init__(self.message)

    def __str__(self):
        return f"UserHasAlreadyVotedError: {self.message}"


class UserNotFoundError(Exception):
    """
    Exception raised when a requested user is not found in the system.

    Attributes:
        user_id -- id of the user that could not be found
        message -- explanation of the error
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.message = f"User with id {user_id} not found."
        super().__init__(self.message)

    def __str__(self):
        return f"UserNotFoundError: {self.message}"


# Vote-related errors

class VoteNotFoundError(Exception):
    """
    Exception raised when a user's vote cannot be found.

    Attributes:
        user_id -- id of the user whose vote was not found
        message -- explanation of the error
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.message = f"The user with id {user_id} has not voted in the current election."
        super().__init__(self.message)

    def __str__(self):
        return f"VoteNotFoundError: {self.message}"


class VoteOptionNotFoundError(Exception):
    """
    Exception raised when a specified vote option does not exist.

    Attributes:
        vote_option_id -- id of the vote option that could not be found
        message -- explanation of the error
    """
    def __init__(self, vote_option_id):
        self.vote_option_id = vote_option_id
        self.message = f"Vote option with id {vote_option_id} does not exist."
        super().__init__(self.message)

    def __str__(self):
        return f"VoteOptionNotFoundError: {self.message}"
