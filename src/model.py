from ultralytics import YOLO

class BallDetector:
    def __init__(self, model_path="assets/trained_best.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]

        if not results.boxes:
            return None

        best = None
        best_conf = 0

        for b in results.boxes:
            conf = float(b.conf[0])
            if conf > best_conf:
                best_conf = conf
                best = b

        if best is None:
            return None

        x1, y1, x2, y2 = best.xyxy[0].cpu().numpy()
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        return {
            "center": (int(cx), int(cy)),
            "bbox": (int(x1), int(y1), int(x2), int(y2)),
            "conf": best_conf
        }

