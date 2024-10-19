"""
Module Name: election_loader.py
Description: This module contains functionality to load election data from a JSON file.

Classes:
    - Election: Represents an election with its associated details.
    - VoteOption: Represents a vote option in the election.

Functions:
    - load_election: Loads election data from a JSON file and returns an Election object.

Usage:
    Call the load_election function to read election data from the specified JSON file and create an Election object.
"""

import json
import os
from ..models import Election, VoteOption


def load_election():
    """
    Load election data from a JSON file and create an Election object.
    
    Returns:
        Election: An instance of the Election class containing the election data.

    Raises:
        FileNotFoundError: If the election JSON file does not exist.
        KeyError: If the expected data is not found in the JSON file.
    """
    json_file_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "election.json"
    )

    with open(json_file_path, "r") as file:
        data = json.load(file)

    dateISO = data["dateISO"]
    vote_options = [
        VoteOption(
            vo["vote_option_id"], vo["party_name"], vo["candidates"], vo["photo"]
        )
        for vo in data["vote_options"]
    ]
    election_id = data["election_id"]

    return Election(election_id, dateISO, vote_options)
