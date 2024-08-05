# service
import cv2
import tempfile
import mediapipe as mp

def process_video(input_path, output_stream, selected_keypoints):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    capture = cv2.VideoCapture(input_path)

    fps = capture.get(cv2.CAP_PROP_FPS)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_output_file:
        temp_output_path = temp_output_file.name

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width, height))

    KEYPOINTS_NAMES = {
        0: "nose", 1: "left_eye_inner", 2: "left_eye", 3: "left_eye_outer",
        4: "right_eye_inner", 5: "right_eye", 6: "right_eye_outer",
        7: "left_ear", 8: "right_ear", 9: "mouth_left", 10: "mouth_right",
        11: "left_shoulder", 12: "right_shoulder", 13: "left_elbow",
        14: "right_elbow", 15: "left_wrist", 16: "right_wrist",
        17: "left_pinky", 18: "right_pinky", 19: "left_index",
        20: "right_index", 21: "left_thumb", 22: "right_thumb",
        23: "left_hip", 24: "right_hip", 25: "left_knee", 26: "right_knee",
        27: "left_ankle", 28: "right_ankle", 29: "left_heel", 30: "right_heel",
        31: "left_foot_index", 32: "right_foot_index"
    }

    DEFAULT_CONNECTIONS = [
        (0, 1), (0, 2), (1, 3), (2, 4), (5, 6), (5, 7), (7, 9),
        (6, 8), (8, 10), (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
        (6, 12), (5, 11)
    ]

    selected_keypoints_indexes = [index for index, name in KEYPOINTS_NAMES.items() if name in selected_keypoints]

    while capture.isOpened():
        success, frame = capture.read()
        if success:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            annotated_frame = frame.copy()

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                for idx, landmark in enumerate(landmarks):
                    if idx in selected_keypoints_indexes:
                        x = int(landmark.x * width)
                        y = int(landmark.y * height)
                        annotated_frame = cv2.circle(annotated_frame, (x, y), 5, (255, 0, 255), -1)
                        annotated_frame = cv2.putText(
                            annotated_frame, KEYPOINTS_NAMES[idx], (x, y - 10),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
                            color=(255, 0, 255), thickness=2
                        )

                for connection in DEFAULT_CONNECTIONS:
                    start_idx, end_idx = connection
                    if start_idx in selected_keypoints_indexes and end_idx in selected_keypoints_indexes:
                        start = landmarks[start_idx]
                        end = landmarks[end_idx]
                        if start.visibility > 0.5 and end.visibility > 0.5:
                            start_point = (int(start.x * width), int(start.y * height))
                            end_point = (int(end.x * width), int(end.y * height))
                            annotated_frame = cv2.line(annotated_frame, start_point, end_point, (0, 255, 0), 2)

            out.write(annotated_frame)
        else:
            break

    capture.release()
    out.release()

    with open(temp_output_path, 'rb') as f:
        output_stream.write(f.read())
