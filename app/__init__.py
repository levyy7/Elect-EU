from flask import Flask
from flask_pymongo import PyMongo

# Initialize the app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/votes_db"
mongo = PyMongo(app)
