from app import mongo


class UserRepository:
    @staticmethod
    def store_user(user_json):
        mongo.db.users.insert_one(user_json)

    @staticmethod
    def get_all_users():
        return list(mongo.db.users.find({}, {"_id": 0}))

    @staticmethod
    def get_user(user_id):
        user = mongo.db.users.find_one({"user_id": user_id}, {"_id": 0})

        return user

    @staticmethod
    def delete_user(user_id):
        result = mongo.db.users.delete_one({"user_id": user_id})

        return result
