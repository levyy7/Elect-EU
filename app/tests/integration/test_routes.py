import unittest
from app import app


class VoteAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_store_vote_missing_fields(self):
        response = self.app.post("/vote", json={"user_id": "1"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get("error"), "Missing fields")

    def test_store_vote_user_does_not_exist(self):
        response = self.app.post("/vote", json={"user_id": "50", "vote_id": "1"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json.get("error"), "The specified user does not exist"
        )

    def test_store_vote_vote_option_does_not_exist(self):
        user1 = {"user_id": "1", "admin_rights": False}
        # Add User to DB
        self.app.post("/register", json=user1)

        response = self.app.post("/vote", json={"user_id": "1", "vote_id": "10"})
        self.assertEqual(response.status_code, 402)
        self.assertEqual(
            response.json.get("error"), "The specified vote_option does not exist"
        )

    def test_store_vote_user_already_voted(self):
        user1 = {"user_id": "1", "admin_rights": False}
        # Add User to DB
        self.app.post("/register", json=user1)

        # User votes 2 times
        self.app.post("/vote", json={"user_id": "1", "vote_id": "1"})

        response = self.app.post("/vote", json={"user_id": "1", "vote_id": "1"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json.get("error"), "The specified user has already voted"
        )

    def test_store_vote_succesful(self):
        user1 = {"user_id": "1", "admin_rights": False}
        # Add User to DB
        self.app.post("/register", json=user1)

        response = self.app.post("/vote", json={"user_id": "1", "vote_id": "1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("message"), "Vote submitted succesfully")

    def test_get_votes(self):
        response = self.app.get("/votes")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
