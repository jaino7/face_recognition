from flask import Flask, request
import face_recognition
import cv2
import numpy as np

app = Flask(__name__)

# ルートへのPOSTリクエストを処理する関数
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        # アップロードされた画像ファイルを取得する
        image_file = request.files['image']

        # 画像をOpenCVで読み込む
        img = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 顔の特徴値を取得する
        face_encoding = face_recognition.face_encodings(img_rgb)[0]

        # 既知の顔の特徴値リストに追加する
        known_face_encodings.append(face_encoding)
        known_face_names.append("Uploaded Image")

        return '画像がアップロードされました。'
    
    return '画像が見つかりません。'

# 顔認識の処理
@app.route('/recognize')
def recognize():
    video_capture = cv2.VideoCapture(0)

    while True:
        _, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 255, 255), 2)

        cv2.imshow('WebCam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # アップロードされた画像を保存するためのリスト
    known_face_encodings = []
    known_face_names = []

    app.run()
