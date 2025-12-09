from ultralytics import YOLO

class model:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")
        self.target_label = "sports ball"

    def detect(self, frame):
        results = self.model(frame, stream=True)
        best_det = None
        best_conf = 0.0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = self.model.names[cls]
                conf = float(box.conf[0])

                if label != self.target_label:
                    continue

                if conf < best_conf:
                    continue

                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                best_conf = conf
                best_det = {
                    "center": (cx, cy),
                    "bbox": (int(x1), int(y1), int(x2), int(y2)),
                    "cls": cls,
                    "label": label,
                    "conf": conf
                }

        return best_det

