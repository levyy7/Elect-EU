"""
Module: models.py

Description: This module defines user-related classes for an election system,
including User, Admin, Citizen, VoteOption, and Election. It provides
functionalities to represent users and their vote options, as well as
the elections they participate in.
"""

from abc import (
    ABC,
    abstractmethod,
)  # Import abstract base class and abstract method decorators

# Uncommenting this line would allow for datetime functionalities.
# import datetime


class User(ABC):
    """
    Abstract base class representing a user.

    Attributes:
        user_id (str): Unique identifier for the user.
        email (str): Email address of the user.
        password (str): Password for user authentication.
    """

    def __init__(self, user_id, email, password):
        self.user_id = user_id  # Initialize the user_id attribute
        self.email = email  # Initialize the email attribute
        self.password = password  # Initialize the password attribute

    @abstractmethod
    def to_json(self):
        """
        Abstract method to convert user object to JSON format.

        Returns:
            dict: JSON representation of the user.
        """
        pass  # This method must be implemented by subclasses.


class Admin(User):
    """
    Class representing an admin user, inheriting from User.

    Overrides:
        to_json: Converts the Admin object to JSON format, including admin rights.
    """

    def to_json(self):
        """
        Convert Admin object to JSON format.

        Returns:
            dict: JSON representation of the admin user, including admin rights.
        """
        return {
            "email": self.email,  # Include the user's email
            "password": self.password,  # Include the user's password
            "admin_rights": True,  # Indicate that this user has admin rights
            "user_id": self.user_id,  # Include the user's ID
        }


class Citizen(User):
    """
    Class representing a regular citizen user, inheriting from User.

    Overrides:
        to_json: Converts the Citizen object to JSON format, indicating no admin rights.
    """

    def to_json(self):
        """
        Convert Citizen object to JSON format.

        Returns:
            dict: JSON representation of the citizen user, without admin rights.
        """
        return {
            "email": self.email,  # Include the user's email
            "password": self.password,  # Include the user's password
            "admin_rights": False,  # Indicate that this user does not have admin rights
            "user_id": self.user_id,  # Include the user's ID
        }


class VoteOption:
    """
    Class representing a voting option in an election.

    Attributes:
        id (str): Unique identifier for the voting option.
        party_name (str): Name of the party associated with this vote option.
        candidates (list): List of candidates for this voting option.
        photo (str): URL or path to the photo representing this voting option.
    """

    def __init__(self, vote_option_id, party_name, candidates, photo):
        self.id = vote_option_id  # Initialize the vote option ID
        self.party_name = party_name  # Initialize the party name
        self.candidates = candidates  # Initialize the list of candidates
        self.photo = photo  # Initialize the photo associated with this vote option

    def to_json(self):
        """
        Convert VoteOption object to JSON format.

        Returns:
            dict: JSON representation of the voting option.
        """
        return {
            "vote_option_id": self.id,  # Include the vote option ID
            "party_name": self.party_name,  # Include the party name
            "candidates": self.candidates,  # Include the list of candidates
            "photo": self.photo,  # Include the photo
        }


class Election:
    """
    Class representing an election.

    Attributes:
        id (str): Unique identifier for the election.
        dateISO (str): ISO format date for the election.
        vote_options (list): List of VoteOption objects associated with this election.
    """

    def __init__(self, election_id, dateISO, vote_options):
        self.id = election_id  # Initialize the election ID
        self.dateISO = dateISO  # Initialize the election date in ISO format
        self.vote_options = vote_options  # Initialize the list of vote options

    def to_json(self):
        """
        Convert Election object to JSON format.

        Returns:
            dict: JSON representation of the election, including its vote options.
        """
        # Convert each VoteOption in the list to JSON format
        vote_options_json = [vote_option.to_json() for vote_option in self.vote_options]
        return {
            "election_id": self.id,  # Include the election ID
            "date": self.dateISO,  # Include the election date
            # Include the list of vote options in JSON format
            "vote_options": vote_options_json,
        }
