"""
Module: user_service.py

Description: This module defines the `UserService` class, responsible for user-related
operations, such as creating, retrieving, and deleting users. It interacts with the
`UserRepository` for database operations and handles both regular citizens and admin
users. The class also manages specific user-related exceptions.

Classes:
    - UserService: Provides methods for creating users, retrieving all users, fetching
      a user by ID, and deleting a user.

Methods:
    - create_user(data, admin_rights=False): Creates a new user (or admin) based on
        the provided data.
    - get_all_users(): Fetches all users from the repository.
    - get_user(user_id): Retrieves a single user by their user ID, raises
        `UserNotFoundError` if not found.
    - delete_user(user_id): Deletes a user by their user ID, raises `UserNotFoundError`
        if the user does not exist.

Dependencies:
    - Citizen, Admin: User models representing different user roles.
    - UserRepository: The repository class used for user-related database operations.
    - UserNotFoundError, UserAlreadyExistsError: Custom exceptions for
        user-related errors.
"""

from ..models import Citizen, Admin
from ..repositories.user_repository import UserRepository
from ..exceptions.error_classes import UserNotFoundError, UserAlreadyExistsError


class UserService:
    """
    Service class responsible for handling user-related operations.
    Interacts with the `UserRepository` to manage user data in the database.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the `UserService` with a `UserRepository` instance.

        :param user_repository: An instance of `UserRepository` to manage user
            database interactions.
        """
        self.user_repository = user_repository

    def create_user(self, data, admin_rights=False):
        """
        Creates a new user (Citizen or Admin) based on the provided data.

        :param data: Dictionary containing user data (user_id, email, password).
        :param admin_rights: Boolean flag indicating whether the user is an admin
            (default is False).
        :raises UserAlreadyExistsError: If a user with the provided `user_id`
            already exists.
        """
        # Fetch all users from the repository to check for existing users
        all_users = self.user_repository.get_all_users()

        # Extract necessary fields from the input data
        email, password, user_id = (
            data.get("email"),
            data.get("password"),
            data.get("user_id"),
        )

        # Check if a user with the given `user_id` already exists
        if any(user.get("user_id") == user_id for user in all_users):
            raise UserAlreadyExistsError(user_id)

        # Create an Admin user if `admin_rights` is True, otherwise create a Citizen
        if admin_rights:
            user = Admin(user_id, email, password)
        else:
            user = Citizen(user_id, email, password)

        # Store the new user in the repository as JSON
        self.user_repository.store_user(user.to_json())

    def get_all_users(self):
        """
        Retrieves all users from the database.

        :return: A list of all users in the database.
        """
        return self.user_repository.get_all_users()

    def get_user(self, user_id):
        """
        Fetches a user by their `user_id`.

        :param user_id: The unique identifier of the user to retrieve.
        :return: The user data as a dictionary.
        :raises UserNotFoundError: If no user is found with the given `user_id`.
        """
        # Fetch the user from the repository
        user = self.user_repository.get_user(user_id)

        # Raise an error if the user is not found
        if not user:
            raise UserNotFoundError(user_id)

        return user

    def delete_user(self, user_id):
        """
        Deletes a user by their `user_id`.

        :param user_id: The unique identifier of the user to delete.
        :raises UserNotFoundError: If no user is found with the given `user_id`.
        """
        # Attempt to delete the user from the repository
        result = self.user_repository.delete_user(user_id)

        # If no user was deleted, raise a `UserNotFoundError`
        if result == 0:
            raise UserNotFoundError(user_id)
