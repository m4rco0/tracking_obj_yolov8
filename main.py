from ultralytics import YOLO
import cv2 as cv
stream_cam = 0
# Carregar o modelo YOLO
model = YOLO('yolov8n.pt')
# pegando a camera que vai representar o frame
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro de caputura")
        break
    results = model.track(frame, persist=True)

    for result in results:
        frame = result.plot()
    cv.imshow('Esp32 tracking', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
