import cv2

def frame_to_ascii(frame, width=40):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    aspect = h / w
    height = int(width * aspect * 0.45)
    height = max(4, height)
    resized = cv2.resize(gray, (width, height))
    chars = "@%#*+=:-. "
    out = []
    for row in resized:
        out.append("".join(chars[int(v/255*(len(chars)-1))] for v in row))
    return out
