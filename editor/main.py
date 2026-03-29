# editor/main.py has been truncated. Recreating full file with proper imports.

import sys, os
sys.path.append(os.path.abspath("."))

import curses
import json
from pathlib import Path
from config import DEFAULT_LEVEL_SIZES, ENTITY_MAP, TILE_OPTIONS

LEVELS_DIR = Path("levels")
LEVELS_DIR.mkdir(exist_ok=True)


def list_levels():
    levels = []
    for p in LEVELS_DIR.glob("*.json"):
        try:
            data = json.load(p)
            name = data.get("name", p.stem)
        except Exception:
            name = p.stem
        if p.name.startswith("custom_"):
            name += " (Custom)"
        levels.append((p, name))
    return levels


class Editor:
    def __init__(self, stdscr, width=20, height=10, level_path=None, level_data=None):
        self.stdscr = stdscr
        self.width = width
        self.height = height
        if level_data is not None:
            tiles = level_data["tiles"]
            self.tiles = [list(row) for row in tiles]
            self.entities = level_data.get("entities", [])
        else:
            self.tiles = [["#" if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1 else "." for x in range(self.width)] for y in range(self.height)]
            self.entities = []
        self.cursor_x = 0
        self.cursor_y = 0
        self.level_path = level_path

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
        max_y, max_x = self.stdscr.getmaxyx()
        for y, row in enumerate(self.tiles):
            if y >= max_y:
                break
            line = "".join(row)[:max_x]
            self.stdscr.addstr(y, 0, line)
        for e in self.entities:
            if e["y"] < max_y and e["x"] < max_x:
                self.stdscr.addch(e["y"], e["x"], e["char"])
        if self.cursor_y < max_y and self.cursor_x < max_x:
            self.stdscr.addch(self.cursor_y, self.cursor_x, "X", curses.A_REVERSE)
        if self.height + 1 < max_y:
            self.stdscr.addstr(self.height + 1, 0, "[1] floor (.)  [0] wall (#)  [@] player  [M] monster  [s] save  [q] quit")
        self.stdscr.refresh()

    def place_entity(self, char):
        if char == "@":
            self.entities = [e for e in self.entities if not (e["char"] == "@" and (e["x"] != self.cursor_x or e["y"] != self.cursor_y))]
        self.entities.append({"x": self.cursor_x, "y": self.cursor_y, "char": char})

    def save(self):
        curses.echo()
        self.stdscr.addstr(self.height + 3, 0, "Enter level name: ")
        self.stdscr.clrtoeol()
        name_bytes = self.stdscr.getstr(self.height + 3, len("Enter level name: "))
        name = name_bytes.decode()
        curses.noecho()
        filename = f"custom_{name}.json"
        path = LEVELS_DIR / filename
        data = {
            "name": name,
            "tiles": ["".join(row) for row in self.tiles],
            "entities": [e for e in self.entities],
        }
        path.write_text(json.dumps(data, indent=2))
        self.stdscr.addstr(self.height + 5, 0, f"Saved to {path}")
        self.stdscr.getch()


def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    selected = 0
    while True:
        stdscr.clear()
        levels = list_levels()
        stdscr.addstr(0, 0, "Level editor – main menu (q to quit)")
        for idx, (p, name) in enumerate(levels):
            marker = "\u003e " if idx == selected else "  "
            stdscr.addstr(2 + idx, 0, f"{marker}{name}")
        stdscr.addstr(2 + len(levels) + 1, 0, "n: New level")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == curses.KEY_UP:
            selected = max(0, selected - 1)
        elif key == curses.KEY_DOWN:
            selected = min(len(levels) - 1, selected + 1)
        elif key in (10, 13):
            if levels:
                path, _ = levels[selected]
                with open(path) as f:
                    data = json.load(f)
                editor = Editor(stdscr, level_path=path, level_data=data)
                editor.run()
        elif key == ord("n"):
            create_new_level(stdscr)


def create_new_level(stdscr):
    curses.echo()
    stdscr.addstr(0, 0, "Choose size: (s)mall (m)edium (l)arge\n")
    choice = stdscr.getch()
    if choice == ord('s'):
        width, height = DEFAULT_LEVEL_SIZES["small"]
    elif choice == ord('m'):
        width, height = DEFAULT_LEVEL_SIZES["medium"]
    else:
        width, height = DEFAULT_LEVEL_SIZES["large"]
    curses.noecho()
    editor = Editor(stdscr, width=width, height=height)
    editor.run()


if __name__ == "__main__":
    curses.wrapper(main_menu)
