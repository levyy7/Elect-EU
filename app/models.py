from abc import ABC, abstractmethod

# import datetime


class User(ABC):
    def __init__(self, user_id):
        self.id = user_id

    @abstractmethod
    def to_json(self):
        pass


class Admin(User):

    def to_json(self):
        return {"user_id": self.id, "admin_rights": True}


class Citizen(User):

    def to_json(self):
        return {"user_id": self.id, "admin_rights": False}


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
    def __init__(self, dateISO, vote_options):
        self.dateISO = dateISO
        self.vote_options = vote_options

    def to_json(self):
        vote_options_json = [vote_option.to_json() for vote_option in self.vote_options]
        return {"dateISO": self.dateISO, "vote_options": vote_options_json}