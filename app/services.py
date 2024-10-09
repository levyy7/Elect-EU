import jwt
import datetime

from app import mongo
from app.models import Vote, User


class VoteService:
    @staticmethod
    def store_vote(vote: Vote):
        mongo.db.votes.insert_one(vote.to_json())

    @staticmethod
    def get_all_votes():
        return list(mongo.db.votes.find({}, {"_id": 0}))

class AuthService:
    SECRET_KEY = 'test123'

    @staticmethod
    def create_token(user: User):
        payload = {
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, AuthService.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=["HS256"])
            return payload["username"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
