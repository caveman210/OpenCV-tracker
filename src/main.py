import cv2
from camcorder import camcorder
from model import model
from kalman import KalmanTracker
from homography_utils import compute_homography, image_to_ground, ground_to_image
from physics_predictor import PhysicsPredictor
from source_selector import choose_source

cam = choose_source()
camera = camcorder(cam)
detector = model()
kt = KalmanTracker()
phys = PhysicsPredictor()

src_points = [
    [100, 200],
    [500, 200],
    [520, 400],
    [80, 400]
]

dst_points = [
    [0.0, 0.0],
    [2.0, 0.0],
    [2.0, 3.0],
    [0.0, 3.0]
]

H, Hinv = compute_homography(src_points, dst_points)

while True:
    success, frame = camera.read()
    if not success:
        break

    det = detector.detect(frame)

    if det is not None:
        cx, cy = det["center"]
        x1, y1, x2, y2 = det["bbox"]

        cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

        gx, gy = image_to_ground(H, cx, cy)

        fx_g, fy_g = kt.update(gx, gy)

        fx_img, fy_img = ground_to_image(Hinv, fx_g, fy_g)
        cv2.circle(frame, (fx_img, fy_img), 6, (0, 0, 255), 2)

        vxg = float(kt.kf.statePost[2, 0])
        vyg = float(kt.kf.statePost[3, 0])

        trajectory, bounce_count, final_rest, max_heights = phys.simulate(
            fx_g, fy_g, vxg, vyg
        )

        for gx_p, gy_p, gz_p in trajectory:
            px_img, py_img = ground_to_image(Hinv, gx_p, gy_p)
            cv2.circle(frame, (px_img, py_img), 2, (255, 0, 0), -1)

        rest_x_img, rest_y_img = ground_to_image(Hinv, final_rest[0], final_rest[1])
        cv2.circle(frame, (rest_x_img, rest_y_img), 6, (0, 255, 255), -1)

        text = f"bounces: {bounce_count}"
        cv2.putText(frame, text, (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.imshow("YOLO + Kalman + Physics", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

