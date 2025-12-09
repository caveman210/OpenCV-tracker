import cv2
import numpy as np

def compute_homography(src_points, dst_points):
    src = np.array(src_points, dtype=np.float32)
    dst = np.array(dst_points, dtype=np.float32)
    H, _ = cv2.findHomography(src, dst)
    H = np.asarray(H, dtype=np.float64)
    Hinv = np.linalg.inv(H)
    return H, Hinv

def image_to_ground(H, x, y):
    p = np.array([x, y, 1.0], dtype=np.float32).reshape(3, 1)
    gp = H @ p
    gp /= gp[2, 0]
    gx, gy = float(gp[0, 0]), float(gp[1, 0])
    return gx, gy

def ground_to_image(Hinv, gx, gy):
    p = np.array([gx, gy, 1.0], dtype=np.float32).reshape(3, 1)
    ip = Hinv @ p
    ip /= ip[2, 0]
    ix, iy = int(ip[0, 0]), int(ip[1, 0])
    return ix, iy

