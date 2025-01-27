"""
Description: Exception for when required fields are missing in a request or operation.
"""


class MissingFieldsError(Exception):
    def __init__(self):
        self.message = "Missing fields."
        super().__init__(self.message)

    def __str__(self):
        return f"MissingFieldsError: {self.message}"
