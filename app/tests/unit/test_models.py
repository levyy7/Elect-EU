import unittest
from app.models import Citizen, Admin, VoteOption, Election


class TestCitizenModel(unittest.TestCase):
    def test_create_citizen(self):
        citizen = Citizen(user_id="1")
        self.assertEqual(citizen.id, "1")

    def test_citizen_to_json(self):
        citizen = Citizen(user_id="1")
        expected_json = {"user_id": "1", "admin_rights": False}
        self.assertEqual(citizen.to_json(), expected_json)


class TestAdminModel(unittest.TestCase):
    def test_create_Admin(self):
        admin = Admin(user_id="1")
        self.assertEqual(admin.id, "1")

    def test_citizen_to_json(self):
        admin = Admin(user_id="1")
        expected_json = {"user_id": "1", "admin_rights": True}
        self.assertEqual(admin.to_json(), expected_json)


class TestVoteOptionModel(unittest.TestCase):
    def test_create_vote_option(self):
        vote_option = VoteOption(
            vote_option_id="1",
            party_name="party1",
            candidates=["name0", "name1"],
            photo="photo1",
        )
        self.assertEqual(vote_option.id, "1")
        self.assertEqual(vote_option.party_name, "party1")
        self.assertEqual(vote_option.candidates, ["name0", "name1"])
        self.assertEqual(vote_option.photo, "photo1")

    def test_vote_option_to_json(self):
        vote_option = VoteOption(
            vote_option_id="1",
            party_name="party1",
            candidates=["name0", "name1"],
            photo="photo1",
        )
        expected_json = {
            "vote_option_id": 1,
            "party_name": "party1",
            "candidates": ["name0", "name1"],
            "photo": "photo1",
        }
        self.assertEqual(vote_option.to_json(), expected_json)


class TestElectionModel(unittest.TestCase):
    def test_election_to_json(self):
        vote_option1 = VoteOption(
            vote_option_id="1",
            party_name="party1",
            candidates=["name0", "name1"],
            photo="photo1",
        )
        vote_option2 = VoteOption(
            vote_option_id="2",
            party_name="party2",
            candidates=["name0", "name1"],
            photo="photo2",
        )
        vote_option3 = VoteOption(
            vote_option_id="3",
            party_name="party3",
            candidates=["name0", "name1"],
            photo="photo3",
        )
        election = Election(
            dateISO="06-10-2024",
            vote_options=[vote_option1, vote_option2, vote_option3],
        )

        expected_json = {
            "dateISO": "06-10-2024",
            "vote_options": [
                {
                    "vote_option_id": 1,
                    "party_name": "party1",
                    "candidates": ["name0", "name1"],
                    "photo": "photo1",
                },
                {
                    "vote_option_id": 2,
                    "party_name": "party2",
                    "candidates": ["name0", "name1"],
                    "photo": "photo2",
                },
                {
                    "vote_option_id": 3,
                    "party_name": "party3",
                    "candidates": ["name0", "name1"],
                    "photo": "photo3",
                },
            ],
        }

        self.assertEqual(election.to_json(), expected_json)


if __name__ == "__main__":
    unittest.main()
