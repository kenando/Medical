from flask import Blueprint
from app.controllers import video_controller

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return video_controller.index()


@main.route('/video', methods=['POST'])
def upload_file():
    return video_controller.upload_file()
