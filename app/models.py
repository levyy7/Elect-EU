from abc import ABC, abstractmethod

# import datetime


class User(ABC):
    def __init__(self, email, password, bsn=None):
        self.email = email
        self.password = password
        self.bsn = bsn

    @abstractmethod
    def to_json(self):
        pass


class Admin(User):
    def to_json(self):
        return {
            "email": self.email,
            "password": self.password,
            "admin_rights": True,
            "BSN": self.bsn,
        }


class Citizen(User):
    def to_json(self):
        return {
            "email": self.email,
            "password": self.password,
            "admin_rights": False,
            "BSN": self.bsn,
        }


class VoteOption:
    def __init__(self, vote_option_id, party_name, candidates, photo):
        self.id = vote_option_id
        self.party_name = party_name
        self.candidates = candidates
        self.photo = photo

    def to_json(self):
        return {
            "vote_option_id": self.id,
            "party_name": self.party_name,
            "candidates": self.candidates,
            "photo": self.photo,
        }


class Election:
    def __init__(self, election_id, dateISO, vote_options):
        self.id = election_id
        self.dateISO = dateISO
        self.vote_options = vote_options

    def to_json(self):
        vote_options_json = [
            vote_option.to_json() for vote_option in self.vote_options
        ]
        return {
            "election_id": self.id,
            "date": self.dateISO,
            "vote_options": vote_options_json,
        }
