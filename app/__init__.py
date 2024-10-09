from flask import Flask
from flask_pymongo import PyMongo
from flask_injector import FlaskInjector
from injector import Binder, singleton
from app.services.user_service import UserService
from app.services.vote_service import VoteService
from app.services.election_service import ElectionService
from app.repositories.user_repository import UserRepository
from app.repositories.vote_repository import VoteRepository

# Initialize the app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/votes_db"
mongo = PyMongo(app)


def configure(binder: Binder):
    binder.bind(UserService, to=UserService(UserRepository(mongo)), scope=singleton)
    binder.bind(
        VoteService,
        to=VoteService(UserRepository(mongo), VoteRepository(mongo)),
        scope=singleton,
    )
    binder.bind(ElectionService, to=ElectionService(), scope=singleton)


from app.controllers.citizen_controller import blueprint_citizen
from app.controllers.admin_controller import blueprint_admin


def register_routes(app):
    # Register all your blueprints here
    app.register_blueprint(blueprint_citizen, url_prefix="")
    app.register_blueprint(blueprint_admin, url_prefix="")


register_routes(app)

# Set up Flask-Injector for dependency injection
FlaskInjector(app=app, modules=[configure])
