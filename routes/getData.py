from flask import Blueprint
from controllers.controllers import get_all_videos ,updateSubtitles,uploadFile, get_video_with_subtitle, download_file

dataRoutes = Blueprint('dataRoutes', __name__)

dataRoutes.route("/uploadFile", methods=["POST"])(uploadFile)
dataRoutes.route("/get_all_videos", methods=["GET"])(get_all_videos)
dataRoutes.route("/get_video_with_subtitle/<video_id>", methods=["GET"])(get_video_with_subtitle)
dataRoutes.route("/download/<filename>", methods=["GET"])(download_file)
dataRoutes.route("/upldateSubtitles", methods=["PUT"])(updateSubtitles)
