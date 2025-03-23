from threading import Thread
import threading
import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils import logging, threaded
class camera:
    def __init__(self, fps=20, capture_cam=0) -> None:
        self.fps = fps
        self.capture_cam = capture_cam
        self.cap =  cv.VideoCapture(self.capture_cam)
        self.frames = []
        self.running = False
        self.model = YOLO("yolov8n.pt")
        self.lock = threading.Lock()

    def run(self):
        logging.debug("Criando o thread")
        self.running = True
        Thread(target=self._capture_loop).start()
        Thread(target=self._process_loop).start()
    def _capture_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            with self.lock:
                if len(self.frames) < 10:
                    self.frames.append(frame)
        self.cap.release()

    def _process_loop(self):
        while self.running:
            if len(self.frames) > 0:
                with self.lock:
                    frame = self.frames.pop(0)
                resultados = self.model.track(frame)
                obj_box = resultados[0].plot()
                cv.imshow("ESP32 ", obj_box)

            key = cv.waitKey(1)
            if key == ord('q') or key == 27:
                self.running = False
                break
        cv.destroyAllWindows()
    def stopCam(self):
        self.running = False

test = camera()
test.run()
