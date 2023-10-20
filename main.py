import json
import keras
from dataset import extract_letters
import cv2
import numpy as np
from flask import Flask, render_template, Response
import cv2
import time

with open("encodes.json", 'r') as file:
    encodes = json.load(file)
model = keras.models.load_model('emnist_letters.h5')
app = Flask(__name__)
camera = cv2.VideoCapture("2.mp4")
green = (50, 255, 0)




def generate_frames():
    start_time = time.time()
    while True:

        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:

            if time.time() - start_time > 0.2:
                start_time = time.time()
                letters = extract_letters(frame)

                for i in letters:
                    img_arr = np.expand_dims(i[1], axis=0)
                    # img_arr = img_arr / 255.0

                    # img_arr = img_arr.reshape((1, 28, 28, 1))
                    predict = model.predict([img_arr])
                    result = np.argmax(predict, axis=1)
                    text = chr(encodes[str(result[0])])
                    cv2.rectangle(frame, (i[0][0], i[0][1]), (i[0][0] + i[0][2], i[0][1] + i[0][3]), green, 3)
                    cv2.putText(frame, text, (i[0][0], i[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 2, green, 3)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
