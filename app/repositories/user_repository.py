from injector import inject


class UserRepository:
    @inject
    def __init__(self, mongo):
        self.mongo = mongo
        self.users_table = mongo.cx.votes_db.users

    def store_user(self, user_json):
        """Store a new user based on their BSN."""

        # Ensure the BSN is present before storing the user
        if not user_json.get("BSN"):
            raise ValueError("BSN is required to store a user.")

        # Insert the user into the users collection
        self.users_table.insert_one(user_json)

    def get_all_users(self):
        """Retrieve all users from the user collection."""
        return list(self.users_table.find({}, {"_id": 0}))

    def get_user(self, bsn):
        """Retrieve a user by their BSN."""
        user = self.users_table.find_one({"BSN": bsn}, {"_id": 0})
        return user

    def delete_user(self, bsn):
        """Delete a user by their BSN."""
        result = self.users_table.delete_one({"BSN": bsn})
        return result
