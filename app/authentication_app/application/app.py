"""
Module: app.py
Description: This module initializes and configures a Flask application with MongoDB, 
it sets up dependency injection using Flask-Injector and registers routes for authentication.
It includes both HTTP and HTTPS server configurations, with optional SSL context.

Components:
1. Flask Application: The core web application framework.
2. PyMongo: MongoDB integration for Flask.
3. Flask-Injector: For handling dependency injection.
4. AuthenticationService: Handles user authentication logic.
5. AuthenticationRepository: Manages interaction with the MongoDB user secrets collection.
6. Blueprint Authentication: Contains the authentication routes and controllers.
"""

import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_injector import FlaskInjector
from injector import Binder, singleton
from .services.authentication_service import AuthenticationService
from .repositories.authentication_repository import AuthenticationRepository
from .schemas import user_secrets_schema
from .controllers.authentication_controller import blueprint_authentication

# Certificate and key files for SSL context
cert_file = "/certs/localhost+2.pem"
key_file = "/certs/localhost+2-key.pem"

# Initialize the Flask application
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/votes_db"

# Set up MongoDB connection with Flask-PyMongo
mongo = PyMongo(app)

# Ensure the 'user_secrets' collection exists with the appropriate schema validator
db = mongo.cx.votes_db
if "user_secrets" not in db.list_collection_names():
    db.create_collection("user_secrets", validator=user_secrets_schema)


def configure(binder: Binder):
    """
    Configures dependency injection bindings for Flask-Injector.
    
    Binds the AuthenticationService to an instance of itself, using 
    AuthenticationRepository with MongoDB (PyMongo) as its data source.
    
    Args:
        binder: The injector Binder instance used to define dependencies.
    """
    binder.bind(
        AuthenticationService,
        to=AuthenticationService(AuthenticationRepository(mongo)),
        scope=singleton,
    )


def register_routes(app):
    """
    Registers application routes (blueprints) with the Flask app.

    Args:
        app: The Flask application instance.
    """
    app.register_blueprint(blueprint_authentication, url_prefix="")


# Register the routes in the app
register_routes(app)

# Set up Flask-Injector for dependency injection
FlaskInjector(app=app, modules=[configure])


def run_app():
    """
    Runs the Flask application, with optional SSL context if certificate and key files are present.
    
    If SSL files are found, the app runs in HTTPS mode on port 5001. If not, it falls back to HTTP.
    """
    # Check if the certificate and key files exist for SSL
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print("Running with SSL context")
        app.run(ssl_context=(cert_file, key_file), host="0.0.0.0", port=5001)
    else:
        print("Running without SSL context")
        app.run(host="0.0.0.0", port=5001)


# Entry point: Run the app if this module is executed directly
if __name__ == "__main__":
    run_app()
