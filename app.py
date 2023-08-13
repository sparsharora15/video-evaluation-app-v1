import flask
from flask import jsonify
from flask_pymongo import PyMongo
from routes.getData import dataRoutes
from werkzeug.exceptions import HTTPException
from config import MONGO_URI
from flask_cors import CORS
# app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

def createApp():
    app = flask.Flask(__name__,static_folder=UPLOAD_FOLDER)
    app.config['MONGO_URI'] = MONGO_URI
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    client = PyMongo(app, uri=MONGO_URI)
    db = client.db
    app.register_blueprint(dataRoutes,url_prefix='/')
    return app,db

(app,db) = createApp()
app.secret_key = "ckropkfpoi94ut875738huidhfi473@#$#@#"

CORS(app, support_credentials=True)

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


if __name__ == "__main__":
    app.run(debug=True)
