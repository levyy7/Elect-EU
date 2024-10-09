import unittest
from app import app


class VoteAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_store_vote(self):
        response = self.app.post("/vote", json={"user_id": "1", "vote_id": "123"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("message"), "Vote stored successfully")

    def test_store_vote_missing_fields(self):
        response = self.app.post("/vote", json={"user_id": "1"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get("error"), "Missing fields")

    def test_get_votes(self):
        response = self.app.get("/votes")
        self.assertEqual(response.status_code, 200)

    def test_get_encrypted_votes(self):
        response = self.app.get_raw("/votes")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
