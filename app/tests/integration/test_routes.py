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


class SecurityTestCase(unittest.TestCase):
    def test_encryption_database(self):
        # Post a vote
        response = self.app.post("/vote", json={"user_id": "1", "vote_id": "123"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("message"), "Vote stored successfully")

        # Fetch the vote from the database
        stored_votes = self.app.get_all_votes_raw()

        # Check if the vote is stored in encrypted format
        self.assertIsNotNone(stored_votes)
        self.assertIn("user_id", stored_votes)
        self.assertIn("vote_id", stored_votes)

        # Access the encrypted values
        encrypted_user_id = stored_votes["user_id"]
        encrypted_vote_id = stored_votes["vote_id"]

        # Check that they are not empty
        self.assertTrue(len(encrypted_user_id) > 0)
        self.assertTrue(len(encrypted_vote_id) > 0)

        # Assert that the encrypted values do not match the original inputs
        self.assertNotEqual(encrypted_user_id, "1")
        self.assertNotEqual(encrypted_vote_id, "123")

    def test_decryption_database(self):
        # Post a vote
        response = self.app.post("/vote", json={"user_id": "1", "vote_id": "123"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("message"), "Vote stored successfully")

        # Fetch the vote from the database
        stored_votes = self.app.get_all_votes()

        # Check if the vote is stored
        self.assertIsNotNone(stored_votes)
        self.assertIn("user_id", stored_votes)
        self.assertIn("vote_id", stored_votes)

        # Decrypt the stored values to verify
        decrypted_user_id = (
            self.cipher.decrypt(stored_votes["user_id"].encode()).decode()
        )
        decrypted_vote_id = (
            self.cipher.decrypt(stored_votes["vote_id"].encode()).decode()
        )

        # Assert that the decrypted values match the original inputs
        self.assertEqual(decrypted_user_id, "1")
        self.assertEqual(decrypted_vote_id, "123")


if __name__ == "__main__":
    unittest.main()
