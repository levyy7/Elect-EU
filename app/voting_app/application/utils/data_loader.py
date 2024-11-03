"""
Description: This file contains the functionality to load election data from
a JSON file.
"""


import json
import os
from ..models import Election, VoteOption


def load_election():
    json_file_path = os.path.join(
        os.path.dirname(__file__), "../", "data", "election.json"
    )

    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Extract the date of the election in ISO format.
    date = data["date"]

    # Create VoteOption instances from the loaded vote options data
    vote_options = [
        VoteOption(
            vo["vote_option_id"], vo["party_name"], vo["candidates"], vo["photo"]
        )
        for vo in data["vote_options"]
    ]
    election_id = data["election_id"]

    return Election(election_id, date, vote_options)
