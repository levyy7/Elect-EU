# from ..models import Election, VoteOption
from utils.data_loader import load_election


class ElectionService:
    def __init__(self):
        pass

    def get_current_election(self):
        currentElection = load_election()
        print("after load: ")
        print(currentElection)

        return currentElection.to_json()
