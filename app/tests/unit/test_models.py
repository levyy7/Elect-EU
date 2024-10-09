import unittest
from app.models import Vote


class TestVoteModel(unittest.TestCase):
    def test_create_vote(self):
        vote = Vote(user_id="1", vote_id="123")
        self.assertEqual(vote.user_id, "1")
        self.assertEqual(vote.vote_id, "123")

    def test_vote_to_json(self):
        vote = Vote(user_id="1", vote_id="123")
        expected_json = {"user_id": "1", "vote_id": "123"}
        self.assertEqual(vote.to_json(), expected_json)

    def test_vote_encrypted_json(self):
        vote = Vote(user_id="1", vote_id="123")
        expected_json = {"user_id": "1", "vote_id": "123"}
        self.assertNotEqual(vote.encrypt_json(), expected_json)

    def test_vote_decrypt_json(self):
        vote = Vote(user_id="1", vote_id="123")
        expected_json = {"user_id": "1", "vote_id": "123"}
        encrypted_json = vote.encrypt_json()

        # Ensure the encrypted JSON is not equal to the expected JSON
        self.assertNotEqual(encrypted_json, expected_json)

        # Decrypt the encrypted JSON back to the original format
        decrypted_user_id = vote.decrypt_data(encrypted_json["user_id"])
        decrypted_vote_id = vote.decrypt_data(encrypted_json["vote_id"])

        # Assert
        self.assertEqual(decrypted_user_id, expected_json["user_id"])
        self.assertEqual(decrypted_vote_id, expected_json["vote_id"])


if __name__ == "__main__":
    unittest.main()
