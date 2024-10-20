"""
Module: election_service.py

Description: This module defines the `ElectionService` class, responsible for handling
election-related logic, specifically fetching the current election data.
It interacts with the `load_election` utility function to retrieve the election details
and then returns the data in JSON format.

Methods:
    - get_current_election(): Retrieves the current election data,
      converts it to JSON format and returns it.

Dependencies:
    - load_election: A utility function that loads election data from a data source.
"""

# Import the load_election utility for fetching election data
from ..utils.data_loader import load_election


class ElectionService:
    """
    Service class responsible for election-related operations.
    """

    def __init__(self):
        """
        Initializes the `ElectionService`. Currently, it does not take any parameters.
        """
        pass

    def get_current_election(self):
        """
        Fetches the current election data, converts it to JSON, and returns it.

        :return: The current election data in JSON format
        """
        # Load the current election data using the `load_election` utility function
        currentElection = load_election()

        # Debugging: Print the loaded election data for verification
        print("after load: ")
        print(currentElection)

        # Convert the election data to JSON and return it
        return currentElection.to_json()
