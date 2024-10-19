"""
Module: authentication_repository.py
Description: This module contains the AuthenticationRepository class, which interacts with the MongoDB database
to manage user-related operations such as storing users, retrieving user data, and handling user secrets.

Classes:
1. AuthenticationRepository: Manages user data storage and retrieval operations in the MongoDB database.
"""

from injector import inject


class AuthenticationRepository:
    """
    Repository class for handling user authentication and data management in MongoDB.

    Attributes:
        mongo: An instance of the MongoDB client used for database operations.
        users_table: Collection for storing user data.
        user_secrets_table: Collection for storing user secrets (e.g., authentication tokens).
    """

    @inject
    def __init__(self, mongo):
        """
        Initializes the AuthenticationRepository with the provided MongoDB client.

        Args:
            mongo: An instance of the MongoDB client for database access.
        """
        self.mongo = mongo
        self.users_table = mongo.cx.votes_db.users
        self.user_secrets_table = mongo.cx.votes_db.user_secrets

    def store_user(self, user_json):
        """
        Stores a new user in the database based on the provided user data.

        Args:
            user_json: A dictionary containing user information to be stored.

        Raises:
            ValueError: If the user_id is missing in the provided user data.
        """
        # Ensure the user_id is present before storing the user
        if not user_json.get("user_id"):
            raise ValueError("user_id is required to store a user.")

        # Insert the user into the users collection
        self.users_table.insert_one(user_json)

    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            A list of all users, excluding the internal MongoDB `_id` field.
        """
        return list(self.users_table.find({}, {"_id": 0}))

    def get_user(self, user_id):
        """
        Retrieves a user by their unique user_id.

        Args:
            user_id: The unique identifier for the user.

        Returns:
            A dictionary containing the user data or None if the user is not found.
        """
        user = self.users_table.find_one({"user_id": user_id}, {"_id": 0})
        return user

    def get_user_id_by_email(self, email):
        """
        Retrieves the user_id associated with a given email address.

        Args:
            email: The email address of the user.

        Returns:
            The unique user_id if found, otherwise None.
        """
        user = self.users_table.find_one({"email": email}, {"_id": 0})
        return user.get("user_id")

    def delete_user(self, user_id):
        """
        Deletes a user from the database by their user_id.

        Args:
            user_id: The unique identifier for the user to be deleted.

        Returns:
            The result of the deletion operation.
        """
        result = self.users_table.delete_one({"user_id": user_id})
        return result

    def verify(self, email, password):
        """
        Verifies whether a user exists with the provided email and password.

        Args:
            email: The user's email address.
            password: The user's password.

        Returns:
            True if the user exists and the password matches, otherwise False.
        """
        # Find the user by email
        user = self.get_user_by_email(email)

        # If user is found, compare the provided password with the stored password
        if user and user["password"] == password:
            return True  # The user exists and the password matches
        return False  # User not found or password doesn't match

    def store_totp_secret(self, email, authentication_token):
        """
        Stores the TOTP secret for a user identified by their email.

        Args:
            email: The user's email address.
            authentication_token: The TOTP secret to store.

        Raises:
            ValueError: If the user associated with the email is not found.
        """
        user_id = self.get_user_id_by_email(email)

        # Update or insert the user's TOTP secret
        self.user_secrets_table.update_one(
            {"user_id": user_id},  # Find user by email
            {
                "$set": {
                    "user_id": user_id,
                    "authentication_token": authentication_token,
                    "bearer_token": "",  # Set bearer token to None for new users
                }
            },
            upsert=True,  # Insert the document if it doesn't exist
        )

    def get_all_user_secrets(self):
        """
        Retrieves all user secrets stored in the database.

        Returns:
            A list of all user secrets, excluding the internal MongoDB `_id` field.
        """
        return list(self.user_secrets_table.find({}, {"_id": 0}))

    def get_user_by_email(self, email):
        """
        Retrieves a user by their email address.

        Args:
            email: The user's email address.

        Returns:
            A dictionary containing the user data or None if the user is not found.
        """
        return self.users_table.find_one({"email": email}, {"_id": 0})

    def get_user_secrets(self, email):
        """
        Retrieves the secrets associated with a user identified by their email.

        Args:
            email: The user's email address.

        Returns:
            A dictionary containing the user's secrets.

        Raises:
            ValueError: If no user is found with the given email or if no secrets are found for that user.
        """
        # Get the user_id associated with the given email
        user = self.get_user_by_email(email)

        if not user:
            raise ValueError(f"No user found with email {email}")

        user_id = user.get("user_id")

        # Find the user's secrets based on the user_id
        user_secrets = self.user_secrets_table.find_one(
            {"user_id": user_id}, {"_id": 0}
        )

        if not user_secrets:
            raise ValueError(f"No secrets found for user with email {email}")

        return user_secrets
