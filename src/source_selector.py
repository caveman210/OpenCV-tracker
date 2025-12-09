import curses
import cv2
import threading
import time
from ascii_preview import frame_to_ascii
from file_picker import pick_file

def list_cameras(max_test=10):
    cams = []
    for i in range(max_test):
        cap = cv2.VideoCapture(i)
        ok, _ = cap.read()
        if ok:
            cams.append(i)
        cap.release()
    return cams

class PreviewThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.running = True
        self.lock = threading.Lock()
        self.lines = ["(no preview)"]

    def set_source(self, index):
        with self.lock:
            if self.cap:
                self.cap.release()
            if index is None:
                self.cap = None
                self.lines = ["(no preview)"]
                return
            self.cap = cv2.VideoCapture(index)

    def run(self):
        while self.running:
            with self.lock:
                cap = self.cap
            if cap:
                ok, frame = cap.read()
                if ok:
                    self.lines = frame_to_ascii(frame)
            time.sleep(0.05)

    def stop(self):
        self.running = False
        with self.lock:
            if self.cap:
                self.cap.release()

def tui_menu(stdscr, cams, items, preview):
    curses.curs_set(0)
    idx = 0
    scroll = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        menu_h = len(items)
        for i, text in enumerate(items):
            if i >= h - 20:
                break
            if i == idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(i + 1, 2, text[:w-4])
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(i + 1, 2, text[:w-4])

        start_y = menu_h + 3
        if start_y < h:
            stdscr.addstr(start_y, 2, "Preview:")

        lines = preview.lines
        view_h = h - start_y - 2
        view_h = max(0, view_h)

        if scroll > len(lines) - view_h:
            scroll = max(0, len(lines) - view_h)

        for n in range(view_h):
            y = start_y + 1 + n
            if y >= h: 
                break
            line_idx = scroll + n
            if line_idx < len(lines):
                stdscr.addstr(y, 2, lines[line_idx][:w-4])

        stdscr.refresh()

        if idx < len(cams):
            preview.set_source(cams[idx])
        else:
            preview.set_source(None)

        key = stdscr.getch()

        if key == curses.KEY_UP and idx > 0:
            idx -= 1
        elif key == curses.KEY_DOWN and idx < len(items) - 1:
            idx += 1
        elif key == curses.KEY_PPAGE:
            scroll = max(0, scroll - 3)
        elif key == curses.KEY_NPAGE:
            scroll = min(len(lines), scroll + 3)
        elif key in (10, 13):
            return idx

def choose_source():
    cams = list_cameras()
    items = [f"Camera {c}" for c in cams] + ["Choose video file"]

    curses.wrapper(lambda s: curses.start_color())
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    preview = PreviewThread()
    preview.start()

    choice = curses.wrapper(lambda s: tui_menu(s, cams, items, preview))

    preview.stop()

    if choice < len(cams):
        return cv2.VideoCapture(cams[choice])

    path = pick_file(".")
    return cv2.VideoCapture(path)

