"""
Module: app.py

Description : This module initializes a Flask application, sets up MongoDB
integration using Flask-PyMongo, and configures dependency injection
using Flask-Injector. It also establishes the necessary collections
in the MongoDB database with appropriate schema validation.
"""

import os  # Import the os module for operating system functionalities
from flask import Flask  # Import the Flask class to create a Flask application
from flask_pymongo import PyMongo  # Import PyMongo to work with MongoDB
from flask_injector import (
    FlaskInjector,
)  # Import FlaskInjector for dependency injection
from injector import (
    Binder,
    singleton,
)  # Import Binder and singleton for configuring bindings
from .services.vote_service import VoteService  # Import VoteService from services
from .services.user_service import UserService  # Import UserService from services
from .services.election_service import (
    ElectionService,
)  # Import ElectionService from services
from .repositories.user_repository import (
    UserRepository,
)  # Import UserRepository from repositories
from .repositories.vote_repository import (
    VoteRepository,
)  # Import VoteRepository from repositories
from .schemas import (
    user_schema,  # Import user schema for validation
    vote_option_schema,  # Import vote option schema for validation
    election_schema,  # Import election schema for validation
    votes_schema,  # Import votes schema for validation
    candidates_schema,  # Import candidates schema for validation
)
from .controllers.citizen_controller import (
    blueprint_citizen,
)  # Import citizen controller blueprint
from .controllers.admin_controller import (
    blueprint_admin,
)  # Import admin controller blueprint

# Paths for SSL certificate and key files
cert_file = "/certs/localhost+2.pem"
key_file = "/certs/localhost+2-key.pem"

# Initialize the Flask application
app = Flask(__name__)
app.config[
    "MONGO_URI"
] = "mongodb://mongo:27017/votes_db"  # Set the MongoDB URI configuration

mongo = PyMongo(app)  # Initialize PyMongo with the Flask app

# Access the votes_db database
db = mongo.cx.votes_db

# Create collections with schema validation if they do not already exist
if "users" not in db.list_collection_names():
    db.create_collection("users", validator=user_schema)  # Create users collection
if "vote_options" not in db.list_collection_names():
    db.create_collection(
        "vote_options", validator=vote_option_schema
    )  # Create vote_options collection
if "candidates" not in db.list_collection_names():
    db.create_collection(
        "candidates", validator=candidates_schema
    )  # Create candidates collection
if "elections" not in db.list_collection_names():
    db.create_collection(
        "elections", validator=election_schema
    )  # Create elections collection
if "votes" not in db.list_collection_names():
    db.create_collection("votes", validator=votes_schema)  # Create votes collection


def configure(binder: Binder):
    """
    Configure dependency injection bindings.

    Args:
        binder (Binder): The binder object used to bind services.
    """
    binder.bind(
        UserService, to=UserService(UserRepository(mongo)), scope=singleton
    )  # Bind UserService
    binder.bind(
        VoteService,
        to=VoteService(UserRepository(mongo), VoteRepository(mongo)),
        scope=singleton,  # Bind VoteService
    )
    binder.bind(
        ElectionService, to=ElectionService(), scope=singleton
    )  # Bind ElectionService


def register_routes(app):
    """
    Register application routes by registering blueprints.

    Args:
        app (Flask): The Flask application instance.
    """
    app.register_blueprint(
        blueprint_citizen, url_prefix=""
    )  # Register citizen controller blueprint
    app.register_blueprint(
        blueprint_admin, url_prefix=""
    )  # Register admin controller blueprint


register_routes(app)  # Call the function to register routes

# Set up Flask-Injector for dependency injection
FlaskInjector(
    app=app, modules=[configure]
)  # Configure Flask-Injector with the application and modules


def run_app():
    """
    Run the Flask application with or without SSL.

    Checks for the existence of certificate and key files to determine
    whether to run the app with SSL context (HTTPS) or not (HTTP).
    """
    # Check if the certificate and key files exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        # If both exist, run the application with SSL context (HTTPS)
        print("Running with SSL context")
        app.run(ssl_context=(cert_file, key_file), host="0.0.0.0", port=5000)
    else:
        # If the files don't exist, run the application without SSL (HTTP)
        print("Running without SSL context")
        app.run(host="0.0.0.0", port=5000)  # Run on all available interfaces


if __name__ == "__main__":
    run_app()  # Run the Flask application when the script is executed directly
