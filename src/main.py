import cv2
from camcorder import camcorder
from model import model
from kalman import KalmanTracker

cam = cv2.VideoCapture(2)
camera = camcorder(cam)

detector = model()

kt = KalmanTracker()

while True:
    success, frame = camera.read()
    if not success:
        break

    det = detector.detect(frame)

    if det is not None:
        (cx, cy) = det["center"]
        (x1, y1, x2, y2) = det["bbox"]

        cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

        fx, fy = kt.update(cx, cy)
        cv2.circle(frame, (fx, fy), 6, (0, 0, 255), 2)

        future_points = kt.predict_trajectory(seconds_ahead=0.5, step=1.0/30.0)
        for (px, py) in future_points:
            cv2.circle(frame, (px, py), 3, (255, 0, 0), -1)

    cv2.imshow("YOLO + Kalman", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

