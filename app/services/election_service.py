# from ..models import Election, VoteOption
from ..utils.data_loader import load_election


class ElectionService:
    @staticmethod
    def get_current_election():
        currentElection = load_election()

        return currentElection.to_json()
