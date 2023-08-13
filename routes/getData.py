from flask import Blueprint
from controllers.controllers import hello_world,get_all_videos ,updaloadFile, get_video, get_video_with_subtitle, download_file

dataRoutes = Blueprint('dataRoutes', __name__)

dataRoutes.route("/", methods=["GET"])(hello_world)
dataRoutes.route("/uploadFile", methods=["POST"])(updaloadFile)
dataRoutes.route("/get_video/<video_id>", methods=["GET"])(get_video)
dataRoutes.route("/get_all_videos", methods=["GET"])(get_all_videos)
dataRoutes.route("/get_video_with_subtitle/<video_id>", methods=["GET"])(get_video_with_subtitle)
dataRoutes.route("/download/<filename>", methods=["GET"])(download_file)
