from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, user_id, email, password):
        self.user_id = user_id
        self.email = email
        self.password = password

    @abstractmethod
    def to_json(self):
        pass


class Admin(User):
    def to_json(self):
        return {
            "email": self.email,
            "password": self.password,
            "admin_rights": True,
            "user_id": self.user_id,
        }


class Citizen(User):
    def to_json(self):
        return {
            "email": self.email,
            "password": self.password,
            "admin_rights": False,
            "user_id": self.user_id,
        }
