"""
Module: vote_repository.py

Description: This module defines the `VoteRepository` class, which is responsible for
performing operations on the `votes` collection in the MongoDB database. The repository
handles storing, retrieving, and deleting votes. Each vote is tied to a
specific user via their `user_id`.

Methods:
    - store_vote(vote_json): Stores a new vote in the `votes` collection.
    - get_all_votes(): Retrieves all votes from the `votes` collection.
    - get_vote_by_voter_id(user_id): Retrieves a specific vote by `user_id`.
    - delete_vote(user_id): Deletes a vote by `user_id`.

Dependencies:
    - mongo: Injected instance of the MongoDB connection through Flask-Injector.
"""

from injector import inject  # Import the injector for dependency injection


class VoteRepository:
    """Repository class to interact with the `votes` collection in MongoDB."""

    @inject
    def __init__(self, mongo):
        """
        Initializes the `VoteRepository` with a MongoDB connection.

        :param mongo: Injected MongoDB connection instance
        """
        self.mongo = mongo  # Store the injected MongoDB connection
        self.votes_table = (
            mongo.cx.votes_db.votes
        )  # Reference to the 'votes' collection in 'votes_db'

    def store_vote(self, vote_json):
        """
        Store a new vote in the `votes` collection.

        :param vote_json: Dictionary containing the vote data (must include `user_id`)
        """
        self.votes_table.insert_one(vote_json)  # Insert the vote into the collection

    def get_all_votes(self):
        """
        Retrieve all votes from the `votes` collection.

        :return: A list of dictionaries representing all votes
        """
        return list(
            self.votes_table.find({}, {"_id": 0})
        )  # Exclude the '_id' field from the result

    def get_vote_by_voter_id(self, user_id):
        """
        Retrieve a specific vote by `user_id` from the `votes` collection.

        :param user_id: The ID of the user who cast the vote
        :return: A dictionary representing the vote, or None if not found
        """
        vote = self.votes_table.find_one(
            {"user_id": user_id}, {"_id": 0}
        )  # Exclude the '_id' field from the result
        return vote

    def delete_vote(self, user_id):
        """
        Delete a vote by `user_id` from the `votes` collection.

        :param user_id: The ID of the user whose vote should be deleted
        :return: The result of the delete operation
        """
        result = self.votes_table.delete_one(
            {"user_id": user_id}
        )  # Perform the delete operation
        return result
