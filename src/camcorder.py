import cv2

class camcorder:
    def __init__(self, cam):
        self.cam = cam

    def read(self):
        return self.cam.read()

    def release(self):
        self.cam.release()

