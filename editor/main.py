"""Simple level editor using curses.

Usage:
  python editor/main.py

The editor lets you paint tiles (# for wall, . for floor) and
place a player (@) or a monster (M).  Press 's' to save to
levels/<name>.json and exit.  'q' quits without saving.
"""

import curses
import json
from pathlib import Path

LEVELS_DIR = Path("levels")
LEVELS_DIR.mkdir(exist_ok=True)

TILE_OPTIONS = {
    0: "#",  # wall
    1: "."   # floor
}

ENTITIES = {
    "@": "player",
    "M": "monster"
}


class Editor:
    def __init__(self, stdscr, width=20, height=10):
        self.stdscr = stdscr
        self.width = width
        self.height = height
        self.tiles = [["#" if x==0 or x==self.width-1 or y==0 or y==self.height-1 else "." for x in range(self.width)] for y in range(self.height)]
        self.entities = []
        self.cursor_x = 0
        self.cursor_y = 0

    def run(self):
        curses.curs_set(0)
        self.stdscr.keypad(True)
        while True:
            self.draw()
            key = self.stdscr.getch()
            if key == ord("q"):
                break
            if key == ord("s"):
                self.save()
                break
            if key in (curses.KEY_UP, ord("w")):
                self.cursor_y = max(0, self.cursor_y - 1)
            elif key == curses.KEY_DOWN:
                self.cursor_y = min(self.height - 1, self.cursor_y + 1)
            elif key in (curses.KEY_LEFT, ord("a")):
                self.cursor_x = max(0, self.cursor_x - 1)
            elif key in (curses.KEY_RIGHT, ord("d")):
                self.cursor_x = min(self.width - 1, self.cursor_x + 1)
            elif key == ord("1"):
                self.tiles[self.cursor_y][self.cursor_x] = TILE_OPTIONS[1]
            elif key == ord("0"):
                self.tiles[self.cursor_y][self.cursor_x] = TILE_OPTIONS[0]
            elif key == ord("@"):
                self.place_entity("@")
            elif key == ord("M"):
                self.place_entity("M")

    def draw(self):
        self.stdscr.clear()
        for y, row in enumerate(self.tiles):
            self.stdscr.addstr(y, 0, "".join(row))
        for e in self.entities:
            self.stdscr.addch(e["y"], e["x"], e["char"])
        self.stdscr.addch(self.cursor_y, self.cursor_x, "X", curses.A_REVERSE)
        self.stdscr.addstr(self.height + 1, 0, "[1] floor (.)  [0] wall (#)  [@] player  [M] monster  [s] save  [q] quit")
        self.stdscr.refresh()

    def place_entity(self, char):
        self.entities = [e for e in self.entities if not (e["char"] == "@" and (e["x"] != self.cursor_x or e["y"] != self.cursor_y))]
        self.entities.append({"x": self.cursor_x, "y": self.cursor_y, "char": char})

    def save(self):
        curses.echo()
        self.stdscr.addstr(self.height + 3, 0, "Enter level name: ")
        self.stdscr.clrtoeol()
        name_bytes = self.stdscr.getstr(self.height + 3, len("Enter level name: "))
        name = name_bytes.decode()
        curses.noecho()
        path = LEVELS_DIR / f"{name}.json"
        data = {
            "name": name,
            "tiles": ["".join(row) for row in self.tiles],
            "entities": [e for e in self.entities]
        }
        path.write_text(json.dumps(data, indent=2))
        self.stdscr.addstr(self.height + 5, 0, f"Saved to {path}")
        self.stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(lambda stdscr: Editor(stdscr).run())
