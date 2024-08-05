# controller
from flask import request, jsonify, send_file
from app.services.video_service import process_video
import tempfile
import io
import json
import os


def index():
    return "Welcome to the Video Processing API!"


def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 一時ファイルに保存
    with tempfile.NamedTemporaryFile(delete=False) as temp_input_file:
        temp_input_file.write(file.read())
        temp_input_path = temp_input_file.name

    output_stream = io.BytesIO()
    selected_keypoints_str = request.form.get('keypoints')  # 選択されたキーポイントを取得
    selected_keypoints = json.loads(selected_keypoints_str)  # JSON文字列をリストに変換
    process_video(temp_input_path, output_stream, selected_keypoints)

    os.remove(temp_input_path)
    output_stream.seek(0)
    return send_file(output_stream, mimetype='video/mp4', as_attachment=True, download_name='output.mp4')
