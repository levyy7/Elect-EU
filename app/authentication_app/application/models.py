"""
Module: models.py
Description: This module defines abstract and concrete user classes to represent different user types in the system.

Classes:
1. User (abstract class): Represents a generic user with basic attributes like user ID, email, and password. This class requires the implementation of a `to_json` method.
2. Admin (concrete class): Inherits from `User` and represents an administrative user with elevated privileges.
3. Citizen (concrete class): Inherits from `User` and represents a regular citizen user without administrative privileges.
"""

from abc import ABC, abstractmethod

class User(ABC):
    """
    Abstract base class representing a generic user.

    Attributes:
        user_id -- unique identifier for the user
        email -- user's email address
        password -- user's password (hashed or encrypted in practice)
    """
    
    def __init__(self, user_id, email, password):
        """
        Initialize a User object with user_id, email, and password.
        
        Args:
            user_id: The unique identifier for the user.
            email: The user's email address.
            password: The user's password.
        """
        self.user_id = user_id
        self.email = email
        self.password = password

    @abstractmethod
    def to_json(self):
        """
        Abstract method to be implemented by subclasses. Converts the user data into JSON format.
        
        Returns:
            A dictionary representing the user's data in JSON-compatible format.
        """
        pass


class Admin(User):
    """
    A class representing an administrative user.

    Inherits from the `User` class and implements the `to_json` method to include additional admin rights.
    """

    def to_json(self):
        """
        Convert the Admin user's data to JSON format, including admin privileges.

        Returns:
            A dictionary containing the user's email, password, admin rights, and user ID.
        """
        return {
            "email": self.email,
            "password": self.password,
            "admin_rights": True,
            "user_id": self.user_id,
        }


class Citizen(User):
    """
    A class representing a citizen user.

    Inherits from the `User` class and implements the `to_json` method to exclude admin rights.
    """

    def to_json(self):
        """
        Convert the Citizen user's data to JSON format, without admin privileges.

        Returns:
            A dictionary containing the user's email, password, admin rights, and user ID.
        """
        return {
            "email": self.email,
            "password": self.password,
            "admin_rights": False,
            "user_id": self.user_id,
        }
