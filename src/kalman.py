import cv2
import numpy as np
import time

class KalmanTracker:
    def __init__(self,
                 process_noise: float = 1e-2,
                 measurement_noise: float = 1e-1):
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=np.float32)
        self.kf.transitionMatrix = np.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * process_noise
        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * measurement_noise
        self.kf.errorCovPost = np.eye(4, dtype=np.float32)
        self.initialized = False
        self.last_time = None

    def _update_dt(self, dt: float):
        self.kf.transitionMatrix = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1,  0],
            [0, 0, 0,  1]
        ], dtype=np.float32)

    def init_state(self, x: float, y: float):
        self.kf.statePost = np.array([[x], [y], [0.0], [0.0]], dtype=np.float32)
        self.initialized = True
        self.last_time = time.time()

    def update(self, x: float, y: float):
        now = time.time()
        if not self.initialized:
            self.init_state(x, y)
            return int(x), int(y)
        dt = now - self.last_time if self.last_time is not None else 0.0
        self.last_time = now
        if dt <= 0.0 or dt > 1.0:
            dt = 1.0 / 30.0
        self._update_dt(dt)
        self.kf.predict()
        measurement = np.array([[np.float32(x)],
                                [np.float32(y)]])
        estimated = self.kf.correct(measurement)
        fx = int(estimated[0, 0])
        fy = int(estimated[1, 0])
        return fx, fy

    def predict_trajectory(self, seconds_ahead: float = 0.5, step: float = 1.0 / 30.0):
        if not self.initialized:
            return []
        dt = step
        F = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1,  0],
            [0, 0, 0,  1]
        ], dtype=np.float32)
        state = self.kf.statePost.copy()
        n_steps = max(1, int(seconds_ahead / step))
        points = []
        for _ in range(n_steps):
            state = F @ state
            px = int(state[0, 0])
            py = int(state[1, 0])
            points.append((px, py))
        return points

