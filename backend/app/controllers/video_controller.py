from flask import request, jsonify, send_file
from app.services.video_service import process_video
import tempfile
import io
import json
import os
import zipfile

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

    video_output_stream = io.BytesIO()
    graph_output_stream = io.BytesIO()
    selected_keypoints_str = request.form.get('keypoints')  # 選択されたキーポイントを取得
    selected_keypoints = json.loads(selected_keypoints_str)  # JSON文字列をリストに変換
    process_video(temp_input_path, video_output_stream, graph_output_stream, selected_keypoints)  # 修正ポイント

    os.remove(temp_input_path)
    video_output_stream.seek(0)
    graph_output_stream.seek(0)

    # Create a zip file containing both the video and the graph
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip_file:
        with zipfile.ZipFile(temp_zip_file, 'w') as zipf:
            zipf.writestr('output.mp4', video_output_stream.read())
            zipf.writestr('graph.png', graph_output_stream.read())
        temp_zip_path = temp_zip_file.name

    return send_file(temp_zip_path, mimetype='application/zip', as_attachment=True, download_name='output.zip')
