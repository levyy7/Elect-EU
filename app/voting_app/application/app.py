import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_injector import FlaskInjector
from injector import Binder, singleton
from .services.vote_service import VoteService
from .services.user_service import UserService
from .services.election_service import ElectionService
from .repositories.user_repository import UserRepository
from .repositories.vote_repository import VoteRepository
from .schemas import (
    user_schema,
    vote_option_schema,
    election_schema,
    votes_schema,
    candidates_schema,
)
from .controllers.citizen_controller import blueprint_citizen
from .controllers.admin_controller import blueprint_admin

cert_file = "/certs/localhost+2.pem"
key_file = "/certs/localhost+2-key.pem"


# Initialize the app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/votes_db"

mongo = PyMongo(app)

db = mongo.cx.votes_db
if "users" not in db.list_collection_names():
    db.create_collection("users", validator=user_schema)
if "vote_options" not in db.list_collection_names():
    db.create_collection("vote_options", validator=vote_option_schema)
if "candidates" not in db.list_collection_names():
    db.create_collection("candidates", validator=candidates_schema)
if "elections" not in db.list_collection_names():
    db.create_collection("elections", validator=election_schema)
if "votes" not in db.list_collection_names():
    db.create_collection("votes", validator=votes_schema)


def configure(binder: Binder):
    binder.bind(UserService, to=UserService(UserRepository(mongo)), scope=singleton)
    binder.bind(
        VoteService,
        to=VoteService(UserRepository(mongo), VoteRepository(mongo)),
        scope=singleton,
    )
    binder.bind(ElectionService, to=ElectionService(), scope=singleton)


def register_routes(app):
    # Register all your blueprints here
    app.register_blueprint(blueprint_citizen, url_prefix="")
    app.register_blueprint(blueprint_admin, url_prefix="")


register_routes(app)

# Set up Flask-Injector for dependency injection
FlaskInjector(app=app, modules=[configure])


def run_app():
    # Check if the certificate and key files exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        # If both exist, run with SSL context (HTTPS)
        print("Running with SSL context")
        app.run(ssl_context=(cert_file, key_file), host="0.0.0.0", port=5000)
    else:
        # If the files don't exist, run without SSL (HTTP)
        print("Running without SSL context")
        app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    run_app()
