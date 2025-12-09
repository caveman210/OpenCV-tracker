import cv2
from model import BallDetector
from kalman import KalmanTracker
from source_selector import choose_source

model = BallDetector("assets/trained_best.pt")
kt = KalmanTracker()

cap = choose_source()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    det = model.detect(frame)

    if det is not None:
        cx, cy = det["center"]
        px, py = kt.update(cx, cy)

        x1, y1, x2, y2 = det["bbox"]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 6, (0, 255, 255), -1)
    else:
        # predicts next position if detection missing
        px, py = kt.update(px, py)

    # draw predicted trajectory using YOUR implementation
    traj = kt.predict_trajectory(seconds_ahead=0.6)

    for tx, ty in traj:
        cv2.circle(frame, (tx, ty), 3, (255, 0, 0), -1)

    cv2.imshow("Tennis Ball Tracker", frame)

    if cv2.waitKey(1) & 0xFF == 'q':
        break

cap.release()
cv2.destroyAllWindows()

