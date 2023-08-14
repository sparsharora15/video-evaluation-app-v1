import random
import string
from flask import current_app
from flask import Flask
from flask import jsonify, request, send_file, send_from_directory
from flask_pymongo import PyMongo
from gridfs import GridFS
from bson import ObjectId, json_util
from bson.json_util import dumps
import json
import os
from .getCollection import returnDBCollection



# @app.route("/")

def hello_world():
    return dumps("hello world")



def updaloadSubtitile(subtitles_file , filename):
    try:
        db = returnDBCollection()
        print("hello")
        collection = db.videos
        if subtitles_file:
            subtitles_data = json.load(subtitles_file)
            collection.insert_one({"subtitles": subtitles_data, "video":filename})
            return jsonify({"message": "Subtitles uploaded successfully"}), 200

        else:
            return jsonify({"message": "No subtitles file provided"}), 400

    except Exception as e:
        return jsonify({"message": "something went wrong"}), 500


# @app.route("/uploadFile", methods=["POST"])
def generate_random_filename():
    # Generate a random string of letters and digits
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return random_string

def updaloadFile():
    try:

        file = request.files["video"]
        subtitles_file = request.files["subtitles"]
        if file.content_type != "video/mp4" and subtitles_file != "application/json":
            return jsonify({"message": "invalid file type", "status_code": 401})
        if file and subtitles_file:
            db = returnDBCollection()
            print("hello")
            collection = db.videos
            subtitles_data = json.load(subtitles_file)
            fileNameToSave = generate_random_filename() + '.mp4'
            filename = os.path.join(current_app.config['UPLOAD_FOLDER'], fileNameToSave)
            file.save(filename)
            collection.insert_one({"subtitles": subtitles_data, "video":fileNameToSave})
            return jsonify({"message": "Subtitles uploaded successfully"}), 200
        else:
            return jsonify({"message": "Please provide both the files"}), 403

    except Exception:
        return jsonify({"message": "something went wrong"}), 500


# @app.route("/get_video/<video_id>", methods=["GET"])
def get_video(video_id):
    try:
        db = returnDBCollection()
        fs = GridFS(db)
        video_id = ObjectId(video_id)
        video_file = fs.get(video_id)
        return send_file(video_file, mimetype=video_file.content_type)

    except Exception as e:
        return jsonify({"message": "something went wrong"}), 500


# @app.route("/get_all_videos", methods=["GET"])
def get_all_videos():
    try:
        db = returnDBCollection()
        data=list(db.videos.find({})) 
        return jsonify({"data": data}), 200

    except Exception as e:
        return jsonify({"message": "something went wrong" ,"err":str(e)}), 500


# @app.route("/get_video_with_subtitle/<video_id>", methods=["GET"])
def get_video_with_subtitle(video_id):
    try:
        db = returnDBCollection()
        fs = GridFS(db)
        video_files = fs.find({"_id": video_id})  # Retrieve all video files
        collection = db.subtitles
        subtitle_files = collection.find_one({"video_id": ObjectId(video_id)})
        print(subtitle_files)

        # Convert video files to a list of dictionaries
        videos = [video_files, subtitle_files]
        if video_files is None:
            return jsonify({"message": "No file found"}), 404

        return dumps({"path": "/uploads", "data": videos[1], "statusCode": 200})

    except Exception as e:
        return jsonify({"message": "something went wrong"}), 500


# @app.route("/download/<filename>")
def download_file(filename):
    try:
        db = returnDBCollection()
        # Specify the path to your static directory
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        return send_from_directory(static_dir, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"message": "something went wrong"}), 500
