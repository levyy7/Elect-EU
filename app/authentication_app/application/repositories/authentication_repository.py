from injector import inject


class AuthenticationRepository:
    @inject
    def __init__(self, mongo):
        self.mongo = mongo
        self.users_table = mongo.cx.votes_db.users
        self.user_secrets_table = mongo.cx.votes_db.user_secrets

    def store_user(self, user_json):
        """Store a new user based on their user_id."""

        # Ensure the user_id is present before storing the user
        if not user_json.get("user_id"):
            raise ValueError("user_id is required to store a user.")

        # Insert the user into the users collection
        self.users_table.insert_one(user_json)

    def get_all_users(self):
        """Retrieve all users from the user collection."""
        return list(self.users_table.find({}, {"_id": 0}))

    def get_user(self, user_id):
        """Retrieve a user by their user_id."""
        user = self.users_table.find_one({"user_id": user_id}, {"_id": 0})
        return user

    def get_user_id_by_email(self, email):
        """Retrieve a user by their user_id."""
        user = self.users_table.find_one({"email": email}, {"_id": 0})
        return user.get("user_id")

    def delete_user(self, user_id):
        """Delete a user by their user_id."""
        result = self.users_table.delete_one({"user_id": user_id})
        return result

    def verify(self, email, password):
        """Verify if a user with the given email and password exists."""
        # Find the user by email
        user = self.get_user_by_email(email)

        # If user is found, compare the provided password with the stored password
        if user and user["password"] == password:
            return True  # The user exists and the password matches
        return False  # User not found or password doesn't match

    def store_totp_secret(self, email, authentication_token):
        user_id = self.get_user_id_by_email(email)

        self.user_secrets_table.update_one(
            {"user_id": user_id},  # Find user by email
            {
                "$set": {
                    "user_id": user_id,
                    "authentication_token": authentication_token,
                    "bearer_token": "",  # Set bearer token to None for new users
                }
            },
            upsert=True,  # Insert the document if it doesn't exist
        )

    def get_all_user_secrets(self):
        """Retrieve all entries from the user_secrets collection."""
        return list(self.user_secrets_table.find({}, {"_id": 0}))

    def get_user_by_email(self, email):
        return self.users_table.find_one({"email": email}, {"_id": 0})

    def get_user_secrets(self, email):
        # Get the user_id associated with the given email
        user = self.get_user_by_email(email)

        if not user:
            raise ValueError(f"No user found with email {email}")

        user_id = user.get("user_id")

        # Find the user's secrets based on the user_id
        user_secrets = self.user_secrets_table.find_one(
            {"user_id": user_id}, {"_id": 0}
        )

        if not user_secrets:
            raise ValueError(f"No secrets found for user with email {email}")

        return user_secrets
