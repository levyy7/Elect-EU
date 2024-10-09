import json
import os
from ..models import Election, VoteOption


def load_election():
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

    return Election(dateISO, vote_options)
