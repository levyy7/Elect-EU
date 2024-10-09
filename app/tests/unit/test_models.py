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
        self.assertNotEqual(encrypted_json, expected_json)
        self.assertEqual(vote.decrypt_data(encrypted_json), expected_json)


if __name__ == "__main__":
    unittest.main()
