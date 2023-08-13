from flask import current_app
from flask_pymongo import PyMongo

def returnDBCollection():
    app = current_app
    db = PyMongo(app).db
    return db