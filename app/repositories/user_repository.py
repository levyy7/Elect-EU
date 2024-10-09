from injector import inject


class UserRepository:
    @inject
    def __init__(self, mongo):
        self.mongo = mongo

    def store_user(self, user_json):
        self.mongo.db.users.insert_one(user_json)

    def get_all_users(self):
        return list(self.mongo.db.users.find({}, {"_id": 0}))

    def get_user(self, user_id):
        user = self.mongo.db.users.find_one({"user_id": user_id}, {"_id": 0})

        return user

    def delete_user(self, user_id):
        result = self.mongo.db.users.delete_one({"user_id": user_id})

        return result
