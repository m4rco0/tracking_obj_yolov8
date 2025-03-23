from ultralytics import YOLO
import cv2 as cv 
from flask import Flask, render_template, request
from werkzeug.wrappers import response
stream_cam = 0
# Carregar o modelo YOLO
# pegando a camera que vai representar o frame
cap = cv.VideoCapture(stream_cam)
model = YOLO('yolov8n.pt')
app = Flask(__name__)

def tracking_obj():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro de caputura")
            break
        results = model.track(frame, persist=True)
        annotade_frame = results[0].plot()
        cv.imshow('Esp32 tracking', annotade_frame)
        key = cv.waitKey(50) & 0xff
        if key == 27 or key == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iniciar_cam')
def iniciar_cam():
    return response.Response(tracking_obj(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
