import cv2
import tempfile


def process_video(input_path, output_stream, selected_keypoints):
    from ultralytics import YOLO
    model = YOLO("yolov8n-pose.pt")

    # 動画のキャプチャを設定
    capture = cv2.VideoCapture(input_path)

    # 動画のプロパティを取得
    fps = capture.get(cv2.CAP_PROP_FPS)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 一時ファイルに保存
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_output_file:
        temp_output_path = temp_output_file.name

    # 動画ライターの設定
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width, height))

    KEYPOINTS_NAMES = {
        0: "nose", 1: "eye(L)", 2: "eye(R)", 3: "ear(L)", 4: "ear(R)",
        5: "shoulder(L)", 6: "shoulder(R)", 7: "elbow(L)", 8: "elbow(R)",
        9: "wrist(L)", 10: "wrist(R)", 11: "hip(L)", 12: "hip(R)",
        13: "knee(L)", 14: "knee(R)", 15: "ankle(L)", 16: "ankle(R)"
    }

    # デフォルトの線の接続を定義
    DEFAULT_CONNECTIONS = [
        (0, 1), (0, 2), (1, 3), (2, 4), (5, 6), (5, 7), (7, 9),
        (6, 8), (8, 10), (11, 12), (11, 13), (13, 15), (12, 14), (14, 16), (6, 12), (5, 11)
    ]

    # selected_keypointsに基づいてインデックスを取得
    selected_keypoints_indexes = [index for index, name in KEYPOINTS_NAMES.items() if name in selected_keypoints]

    while capture.isOpened():
        success, frame = capture.read()
        if success:
            results = model(frame)
            annotatedFrame = frame.copy()  # フレームのコピーを作成

            if results[0].keypoints is not None and results[0].keypoints.conf is not None:
                keypoints = results[0].keypoints
                confs = keypoints.conf[0].tolist()
                xys = keypoints.xy[0].tolist()

                # キーポイントを描画
                for index, keypoint in enumerate(zip(xys, confs)):
                    score = keypoint[1]
                    if score < 0.5:
                        continue

                    if index not in selected_keypoints_indexes:
                        continue

                    x = int(keypoint[0][0])
                    y = int(keypoint[0][1])
                    annotatedFrame = cv2.rectangle(
                        annotatedFrame, (x, y), (x + 3, y + 3), (255, 0, 255), cv2.FILLED, cv2.LINE_AA
                    )
                    annotatedFrame = cv2.putText(
                        annotatedFrame, KEYPOINTS_NAMES[index], (x + 5, y),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.3,
                        color=(255, 0, 255), thickness=2, lineType=cv2.LINE_AA
                    )

                # デフォルトの接続線を描画
                for (start, end) in DEFAULT_CONNECTIONS:
                    if start in selected_keypoints_indexes and end in selected_keypoints_indexes:
                        if confs[start] >= 0.5 and confs[end] >= 0.5:
                            x1, y1 = int(xys[start][0]), int(xys[start][1])
                            x2, y2 = int(xys[end][0]), int(xys[end][1])
                            cv2.line(annotatedFrame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            out.write(annotatedFrame)
        else:
            break

    capture.release()
    out.release()

    # 一時ファイルを出力ストリームに書き込み
    with open(temp_output_path, 'rb') as f:
        output_stream.write(f.read())
