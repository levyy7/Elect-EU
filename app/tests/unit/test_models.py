import unittest
from app.models import Citizen, Admin, VoteOption, Election


class TestCitizenModel(unittest.TestCase):
    def test_create_citizen(self):
        citizen = Citizen(
            user_id=1, email="citizen@example.com", password="password123"
        )
        self.assertEqual(citizen.user_id, 1)
        self.assertEqual(citizen.email, "citizen@example.com")
        self.assertEqual(citizen.password, "password123")

    def test_citizen_to_json(self):
        citizen = Citizen(
            user_id=1, email="citizen@example.com", password="password123"
        )
        expected_json = {
            "user_id": 1,
            "email": "citizen@example.com",
            "password": "password123",
            "admin_rights": False,
        }
        self.assertEqual(citizen.to_json(), expected_json)


class TestAdminModel(unittest.TestCase):
    def test_create_admin(self):
        admin = Admin(user_id=1, email="admin@example.com", password="adminpass")
        self.assertEqual(admin.user_id, 1)
        self.assertEqual(admin.email, "admin@example.com")
        self.assertEqual(admin.password, "adminpass")

    def test_admin_to_json(self):
        admin = Admin(user_id=1, email="admin@example.com", password="adminpass")
        expected_json = {
            "user_id": 1,
            "email": "admin@example.com",
            "password": "adminpass",
            "admin_rights": True,
        }
        self.assertEqual(admin.to_json(), expected_json)


class TestVoteOptionModel(unittest.TestCase):
    def test_vote_option_to_json(self):
        vote_option = VoteOption(
            vote_option_id=1,
            party_name="Party A",
            candidates=["Candidate A", "Candidate B"],
            photo="party_a.png",
        )
        expected_json = {
            "vote_option_id": 1,
            "party_name": "Party A",
            "candidates": ["Candidate A", "Candidate B"],
            "photo": "party_a.png",
        }
        self.assertEqual(vote_option.to_json(), expected_json)


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
            "vote_option_id": "1",
            "party_name": "party1",
            "candidates": ["name0", "name1"],
            "photo": "photo1",
        }
        self.assertEqual(vote_option.to_json(), expected_json)


class TestElectionModel(unittest.TestCase):
    def test_election_to_json(self):
        vote_option1 = VoteOption(
            vote_option_id=1,
            party_name="Party A",
            candidates=["Candidate A", "Candidate B"],
            photo="party_a.png",
        )
        vote_option2 = VoteOption(
            vote_option_id=2,
            party_name="Party B",
            candidates=["Candidate C", "Candidate D"],
            photo="party_b.png",
        )
        election = Election(
            election_id=1,
            dateISO="2024-10-10",
            vote_options=[vote_option1, vote_option2],
        )
        expected_json = {
            "election_id": 1,
            "date": "2024-10-10",
            "vote_options": [
                {
                    "vote_option_id": 1,
                    "party_name": "Party A",
                    "candidates": ["Candidate A", "Candidate B"],
                    "photo": "party_a.png",
                },
                {
                    "vote_option_id": 2,
                    "party_name": "Party B",
                    "candidates": ["Candidate C", "Candidate D"],
                    "photo": "party_b.png",
                },
            ],
        }
        self.assertEqual(election.to_json(), expected_json)


if __name__ == "__main__":
    unittest.main()
