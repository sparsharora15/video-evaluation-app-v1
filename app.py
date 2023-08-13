from flask import Flask
from flask import jsonify, request, send_file, send_from_directory
from flask_pymongo import PyMongo

from config import MONGO_URI

app = Flask(__name__)
from gridfs import GridFS
from bson import ObjectId, json_util
from bson.json_util import dumps
import json
import os

app.secret_key = "ckropkfpoi94ut875738huidhfi473@#$#@#"
from flask_cors import CORS

CORS(app)
mongo = PyMongo(app, uri=MONGO_URI)
fs = GridFS(mongo.db)


@app.route("/")
def hello_world():
    return "Hello, World!"


def updaloadSubtitile(video_id, subtitles_file):
    try:
        print("hello")
        collection = mongo.db.subtitles
        checkVideo = collection.find_one({"video_id": video_id})
        if checkVideo:
            return jsonify({"message": "Subtitles already exists on that video"}), 401
        #  subtitles_file = request.files['subtitles']
        if subtitles_file:
            subtitles_data = json.load(subtitles_file)
            collection.insert_one({"video_id": video_id, "subtitles": subtitles_data})
            return jsonify({"message": "Subtitles uploaded successfully"}), 200

        else:
            return jsonify({"message": "No subtitles file provided"}), 400

    except Exception as e:
        return jsonify({"message": "something went wrong"}), 500


@app.route("/uploadFile", methods=["POST"])
def updaloadFile():
    try:
        file = request.files["video"]
        subtitles_file = request.files["subtitles"]
        if file.content_type != "video/mp4" and subtitles_file != "application/json":
            return jsonify({"message": "invalid file type", "status_code": 401})
        if file:
            video_id = fs.put(
                file, content_type=file.content_type, filename=file.filename
            )
            updaloadSubtitile(video_id, subtitles_file)
            return (
                jsonify(
                    {
                        "message": "Video uploaded successfully",
                        "video_id": str(video_id),
                        "status_code": 200,
                    }
                ),
                200,
            )
        else:
            return jsonify({"message": "No file provided"}), 400

    except Exception:
        return jsonify({"message": "something went wrong"}), 500


@app.route("/get_video/<video_id>", methods=["GET"])
def get_video(video_id):
    try:
        video_id = ObjectId(video_id)
        video_file = fs.get(video_id)
        return send_file(video_file, mimetype=video_file.content_type)

    except Exception as e:
        return jsonify({"message": "something went wrong"}), 500


@app.route("/get_all_videos", methods=["GET"])
def get_all_videos():
    try:
        video_files = fs.find({})  # Retrieve all video files

        # Convert video files to a list of dictionaries
        videos = []
        if video_files is None:
            return jsonify({"message": "No file found"}), 404
        for video_file in video_files:
            videos.append(
                {
                    "video_id": str(video_file._id),
                }
            )
        return jsonify({"path": "/get_video", "data": videos}), 200

    except Exception as e:
        return jsonify({"message": "something went wrong"}), 500


@app.route("/get_video_with_subtitle/<video_id>", methods=["GET"])
def get_video_with_subtitle(video_id):
    try:
        print(video_id)
        video_files = fs.find({"_id": video_id})  # Retrieve all video files
        collection = mongo.db.subtitles
        subtitle_files = collection.find_one({"video_id": ObjectId(video_id)})
        print(subtitle_files)

        # Convert video files to a list of dictionaries
        videos = [video_files, subtitle_files]
        if video_files is None:
            return jsonify({"message": "No file found"}), 404

        return dumps({"path": "/get_video", "data": videos[1], "statusCode": 200})

    except Exception as e:
        return jsonify({"message": "something went wrong"}), 500


@app.route("/download/<filename>")
def download_file(filename):
    try:
        # Specify the path to your static directory
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        return send_from_directory(static_dir, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"message": "something went wrong"}), 500


# if __name__ == "__main__":
#     app.run(debug=True)
