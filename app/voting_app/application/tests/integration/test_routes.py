"""
Description: This file contains unit tests for the voting application,
Testing the endpoints related to storing votes and retrieving votes. 
"""


import unittest
from application.app import app


class VoteAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_store_vote_missing_fields(self):
        response = self.app.post("/vote", json={"user_id": 1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json.get("error"), "MissingFieldsError: Missing fields."
        )

    def test_store_vote_user_does_not_exist(self):
        response = self.app.post("/vote", json={"user_id": 50, "vote_option_id": 1})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json.get("error"), "UserNotFoundError: User with id 50 not found."
        )

    def test_store_vote_vote_option_does_not_exist(self):
        # Register a user first
        user1 = {"user_id": 1, "email": "user1@example.com", "password": "password123"}
        self.app.post("/register", json=user1)

        # Test voting with a non-existing vote option
        response = self.app.post("/vote", json={"user_id": 1, "vote_option_id": 10})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json.get("error"),
            "VoteOptionNotFoundError: Vote option with id 10 does not exist.",
        )

    def test_store_vote_user_already_voted(self):
        user1 = {"user_id": 1, "email": "user1@example.com", "password": "password123"}
        # Add User to DB
        self.app.post("/register", json=user1)

        # User votes 2 times
        self.app.post("/vote", json={"user_id": 1, "vote_id": 1})

        response = self.app.post("/vote", json={"user_id": 1, "vote_option_id": 1})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json.get("error"),
            "UserHasAlreadyVotedError: User with id 1 has "
            + "already voted in the current election.",
        )

    def test_store_vote_success(self):
        user1 = {"user_id": 1, "email": "user1@example.com", "password": "password123"}
        # Add User to DB
        self.app.post("/register", json=user1)

        response = self.app.post("/vote", json={"user_id": 1, "vote_option_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("message"), "Vote submitted succesfully.")

    def test_get_votes(self):
        response = self.app.get("/votes")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
