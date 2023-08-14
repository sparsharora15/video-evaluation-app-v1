import random
import string
from flask import current_app
from flask import jsonify, request, send_file, send_from_directory
from gridfs import GridFS
from bson import ObjectId, json_util
from bson.json_util import dumps
import json
import os
from .getCollection import returnDBCollection


import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name="dw65n4evs",
    api_key="452623662246538",
    api_secret="Li8nDCTGy5iG-BrXQk0dpzGmOfA",
)


def generate_random_filename():
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    return random_string


def uploadFile():
    try:
        file = request.files["video"]
        subtitles_file = request.files["subtitles"]

        if (
            file.content_type != "video/mp4"
            or subtitles_file.content_type != "application/json"
        ):
            return jsonify({"message": "invalid file type", "statusCode": 401})

        if file and subtitles_file:
            subtitles_data = json.load(subtitles_file)

            result = cloudinary.uploader.upload(
                file,
                resource_type="video",
                use_filename=True,
                unique_filename=False,
            )

            db = returnDBCollection()
            collection = db.videos
            collection.insert_one(
                {"subtitles": subtitles_data, "video": result["secure_url"]}
            )

            return (
                jsonify(
                    {
                        "message": "Files uploaded successfully",
                        "fileName": result["secure_url"],
                        "statusCode": 200,
                    }
                ),
                200,
            )

        else:
            return jsonify({"message": "Please provide both the files"}), 403

    except Exception as e:
        return jsonify({"message": "something went wrong", "err": str(e)}), 500


def get_all_videos():
    try:
        db = returnDBCollection()
        data = list(db.videos.find({}))
        serialized_data = json_util.dumps(data)  # Serialize the data
        return serialized_data, 200

    except Exception as e:
        return jsonify({"message": "something went wrong", "err": str(e)}), 500


def get_video_with_subtitle(video_id):
    try:
        db = returnDBCollection()
        data = db.videos.find_one({"_id": ObjectId(video_id)})
        if data is None:
            return jsonify({"message": "No file found"}), 404

        data["_id"] = str(data["_id"])
        return jsonify({"data": data, "statusCode": 200})
        # return jsonify({"data": data, "statusCode": 200})
    except Exception as e:
        return jsonify({"message": "something went wrong" + str(e)}), 500


def download_file(filename):
    try:
        db = returnDBCollection()
        # Specify the path to your static directory
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        return send_from_directory(static_dir, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"message": "something went wrong"}), 500


def updateSubtitles():
    try:
        db = returnDBCollection()
        data = request.json["data"]
        videoId = request.json["videoId"]
        if not data or not videoId:
            return jsonify({"message": "something went wrong"}), 500
        db.videos.find_one_and_update(
            {"_id": ObjectId(videoId)}, {"$set": {"subtitles": data}}
        )
        return jsonify({"message": "subtitles updated successfully","status_code":200})

    except Exception as e:
        return jsonify({"message": "something went wrong", "err": str(e)}), 500
