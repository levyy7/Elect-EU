"""
Description: This file contains unit tests for the voting application,
Testing the endpoints related to storing votes and retrieving votes. 
"""


import unittest
from application.app import app
import jwt
import datetime


class VoteAppTestCase(unittest.TestCase):
    def get_valid_token(self):
        token = jwt.encode(
            {
                "user_id": 1,
                "email": "user1@example.com",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            },
            "your_secret_key",  # Replace this with your actual secret key
            algorithm="HS256",
        )
        return token

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.headers = {"Authorization": f"Bearer {self.get_valid_token()}"}

    def test_store_vote_missing_fields(self):
        response = self.app.post("/vote", headers=self.headers, json={"user_id": 1})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json.get("error"), "MissingFieldsError: Missing fields."
        )

    #
    def test_store_vote_user_does_not_exist(self):
        response = self.app.post(
            "/vote", headers=self.headers, json={"user_id": 1, "vote_option_id": 1}
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json.get("error"), "UserNotFoundError: User with id 1 not found."
        )

    def test_store_vote_vote_option_does_not_exist(self):
        # Register a user first
        user1 = {"user_id": 1, "email": "user1@example.com", "password": "password123"}
        res = self.app.post("/register", json=user1)
        self.assertEqual(res.status_code, 200)

        # Test voting with a non-existing vote option
        response = self.app.post(
            "/vote", headers=self.headers, json={"user_id": 1, "vote_option_id": 10}
        )
        # self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json.get("error"),
            "VoteOptionNotFoundError: Vote option with id 10 does not exist.",
        )

    def test_store_vote_user_already_voted(self):
        # User votes 2 times
        self.app.post(
            "/vote", headers=self.headers, json={"user_id": 1, "vote_option_id": 1}
        )
        response = self.app.post(
            "/vote", headers=self.headers, json={"user_id": 1, "vote_option_id": 1}
        )
        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
