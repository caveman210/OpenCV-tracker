import curses
import os
import fnmatch

def safe_path(p):
    if not p or p == "":
        return "/"
    return p

def fuzzy_filter(query, items):
    if query == "":
        return items
    q = query.lower()
    return [i for i in items if q in i.lower()]

def pick_file(start="."):
    return curses.wrapper(lambda s: _pick(s, safe_path(start)))

def _pick(stdscr, start_path):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    path = start_path
    query = ""
    idx = 0

    while True:
        all_items = [".."] + sorted(os.listdir(path))
        items = fuzzy_filter(query, all_items)
        idx = 0 if idx >= len(items) else idx

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            stdscr.addstr(0, 2, f"Dir: {path[:w-4]}")
            stdscr.addstr(1, 2, f"Search: {query[:w-10]}")

            for i, name in enumerate(items):
                y = i + 3
                if y >= h - 1:
                    break
                line = name[:w-4]
                if i == idx:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, 2, line)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, 2, line)

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and idx > 0:
                idx -= 1
            elif key == curses.KEY_DOWN and idx < len(items) - 1:
                idx += 1
            elif key in (10, 13):
                sel = items[idx]
                if sel == "..":
                    path = safe_path(os.path.dirname(path))
                    break
                full = os.path.join(path, sel)
                if os.path.isdir(full):
                    path = full
                    break
                return full
            elif key == 27:
                return None
            elif 32 <= key <= 126:
                query += chr(key)
                break
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                query = query[:-1]
                break

