"""
Module: user_repository.py

Description: This module defines the UserRepository class, which is responsible for
performing CRUD (Create, Read, Update, Delete) operations on the users collection
in the MongoDB database. It interacts with the `votes_db` database and the `users`
collection to store, retrieve, and delete user data.

Methods:
    - store_user(user_json): Stores a new user in the users collection.
    - get_all_users(): Retrieves all users from the users collection.
    - get_user(user_id): Retrieves a specific user by user_id.
    - delete_user(user_id): Deletes a specific user by user_id.

Dependencies:
    - mongo: Injected instance of the MongoDB connection through Flask-Injector.
"""

from injector import inject  # Import the injector for dependency injection


class UserRepository:
    """Repository class to interact with the users collection in MongoDB."""

    @inject
    def __init__(self, mongo):
        """
        Initializes the UserRepository with a MongoDB connection.

        :param mongo: Injected MongoDB connection instance
        """
        self.mongo = mongo  # Store the injected MongoDB connection
        self.users_table = (
            mongo.cx.votes_db.users
        )  # Reference to the 'users' collection in 'votes_db'

    def store_user(self, user_json):
        """
        Store a new user in the users collection based on their user_id.

        :param user_json: Dictionary containing the user data
        :raises ValueError: If 'user_id' is not present in the user data
        """
        # Ensure the user_id is present before storing the user
        if not user_json.get("user_id"):
            raise ValueError("user_id is required to store a user.")

        # Insert the user into the users collection
        self.users_table.insert_one(user_json)

    def get_all_users(self):
        """
        Retrieve all users from the users collection.

        :return: A list of dictionaries representing all users
        """
        return list(
            self.users_table.find({}, {"_id": 0})
        )  # Exclude the '_id' field from the result

    def get_user(self, user_id):
        """
        Retrieve a user by their user_id from the users collection.

        :param user_id: The ID of the user to be retrieved
        :return: A dictionary representing the user, or None if not found
        """
        user = self.users_table.find_one(
            {"user_id": user_id}, {"_id": 0}
        )  # Exclude the '_id' field from the result
        return user

    def delete_user(self, user_id):
        """
        Delete a user by their user_id from the users collection.

        :param user_id: The ID of the user to be deleted
        :return: The result of the delete operation
        """
        result = self.users_table.delete_one(
            {"user_id": user_id}
        )  # Perform the delete operation
        return result
