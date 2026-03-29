"""Renderer module.

Renders a static tile grid and entity list onto a curses window.
"""

from typing import List


class Renderer:
    def __init__(self, tiles: List[str], entities: List[object]):
        self.tiles = tiles
        self.entities = entities

    def draw(self, stdscr):
        # draw tiles
        for y, row in enumerate(self.tiles):
            stdscr.addstr(y, 0, row)
        # draw entities
        for e in self.entities:
            try:
                # skip drawing a tile if an entity is already on this spot
                if self.tiles[e.y][e.x] == e.char:
                    continue
                stdscr.addch(e.y, e.x, e.char)
            except Exception:
                pass
