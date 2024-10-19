"""
Module: test_vote_app.py

Description: This module contains unit tests for the voting application, specifically
testing the endpoints related to storing votes and retrieving votes. Each test case
verifies the application's behavior under various scenarios, including handling
missing fields, checking user existence, and ensuring that votes are recorded
correctly.
"""

import unittest  # Import the unittest module for creating and running tests
from application.app import app  # Import the Flask application


class VoteAppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client for the application before each test."""
        self.app = app.test_client()  # Create a test client for the app
        self.app.testing = True  # Enable testing mode

    def test_store_vote_missing_fields(self):
        """Test the /vote endpoint with missing fields."""
        response = self.app.post(
            "/vote", json={"user_id": 1}
        )  # Post with missing vote_option_id
        self.assertEqual(response.status_code, 400)  # Expect a 400 Bad Request
        self.assertEqual(
            response.json.get("error"), "MissingFieldsError: Missing fields."
        )  # Check the error message

    def test_store_vote_user_does_not_exist(self):
        """Test the /vote endpoint with a non-existent user."""
        response = self.app.post(
            "/vote", json={"user_id": 50, "vote_option_id": 1}
        )  # User ID doesn't exist
        self.assertEqual(response.status_code, 404)  # Expect a 404 Not Found
        self.assertEqual(
            response.json.get("error"), "UserNotFoundError: User with id 50 not found."
        )  # Check the error message

    def test_store_vote_vote_option_does_not_exist(self):
        """Test the /vote endpoint with a non-existent vote option."""
        user1 = {"user_id": 1, "email": "user1@example.com", "password": "password123"}
        self.app.post("/register", json=user1)  # Register a user first

        response = self.app.post(
            "/vote", json={"user_id": 1, "vote_option_id": 10}
        )  # Non-existing vote option
        self.assertEqual(response.status_code, 404)  # Expect a 404 Not Found
        self.assertEqual(
            response.json.get("error"),
            "VoteOptionNotFoundError: Vote option with id 10 does not exist.",
        )  # Check the error message

    def test_store_vote_user_already_voted(self):
        """Test the /vote endpoint when a user tries to vote more than once."""
        user1 = {"user_id": 1, "email": "user1@example.com", "password": "password123"}
        self.app.post("/register", json=user1)  # Register a user

        self.app.post("/vote", json={"user_id": 1, "vote_option_id": 1})  # First vote

        response = self.app.post(
            "/vote", json={"user_id": 1, "vote_option_id": 1}
        )  # Second vote
        self.assertEqual(response.status_code, 401)  # Expect a 401 Unauthorized
        self.assertEqual(
            response.json.get("error"),
            "UserHasAlreadyVotedError: User with id 1 has "
            + "already voted in the current election.",
        )  # Check the error message

    def test_store_vote_success(self):
        """Test the /vote endpoint for a successful vote submission."""
        user1 = {"user_id": 1, "email": "user1@example.com", "password": "password123"}
        self.app.post("/register", json=user1)  # Register a user

        response = self.app.post(
            "/vote", json={"user_id": 1, "vote_option_id": 1}
        )  # Successful vote
        self.assertEqual(response.status_code, 200)  # Expect a 200 OK
        self.assertEqual(
            response.json.get("message"), "Vote submitted succesfully."
        )  # Check success message

    def test_get_votes(self):
        """Test the /votes endpoint to retrieve votes."""
        response = self.app.get("/votes")  # Retrieve votes
        self.assertEqual(response.status_code, 200)  # Expect a 200 OK


if __name__ == "__main__":
    unittest.main()  # Run the tests when the script is executed directly
