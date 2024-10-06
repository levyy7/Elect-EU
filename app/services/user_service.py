from app import mongo
from flask import jsonify


class UserService:
    @staticmethod
    def store_user(user_json):
        mongo.db.users.insert_one(user_json)

    @staticmethod
    def get_all_users():
        return list(mongo.db.users.find({}, {"_id": 0}))

    @staticmethod
    def get_user(user_id):
        user = mongo.db.users.find_one({"user_id": user_id}, {"_id": 0})

        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
