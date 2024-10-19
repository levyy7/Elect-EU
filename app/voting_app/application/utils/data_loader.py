"""
Module: data_loader.py

Description: This module loads election data from a JSON file and constructs
Election and VoteOption objects based on the loaded data.

It reads the election configuration, including the date and available vote options,
and returns an instance of the Election class populated with the relevant details.
"""

import json  # Import json for handling JSON file reading
import os  # Import os for file path operations
from ..models import Election, VoteOption  # Import Election and VoteOption classes


def load_election():
    """
    Load election data from a JSON file and create an Election object.

    Returns:
        Election: An instance of the Election class populated with
        data from the JSON file.

    Raises:
        FileNotFoundError: If the election JSON file does not exist.
        KeyError: If expected keys are missing in the JSON data.
    """
    # Construct the file path for the election JSON file
    json_file_path = os.path.join(
        os.path.dirname(__file__), "../", "data", "election.json"
    )

    # Open and read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)  # Load the JSON data into a dictionary

    # Extract the date of the election in ISO format
    dateISO = data["dateISO"]

    # Create VoteOption instances from the loaded vote options data
    vote_options = [
        VoteOption(
            vo["vote_option_id"], vo["party_name"], vo["candidates"], vo["photo"]
        )
        for vo in data["vote_options"]
    ]

    # Extract the election ID
    election_id = data["election_id"]

    # Return an instance of the Election class with the loaded data
    return Election(election_id, dateISO, vote_options)
