#!/usr/bin/env python3
"""Main game loop for Timur and his Team ASCII roguelike.

The engine loads a level JSON, creates entities, and runs a simple
curses‑based render loop. Movement is handled with arrow keys or
wasd.  Press 'i' to open the inventory, 'q' to quit, and
Enter to interact with the tile below the player.
"""

import curses
import json
from pathlib import Path
from entities import Entity, Player, Monster
from render import Renderer
from ui.inventory import InventoryUI
from ui.dialogue import DialogueUI
from ui.quest import QuestJournal

# Configuration
LEVELS_DIR = Path("levels")
DEFAULT_LEVEL = "sample.json"


def load_level(name: str):
    """Load a level JSON file and return grid and entities."""
    path = LEVELS_DIR / name
    data = json.loads(path.read_text())
    tiles = data["tiles"]
    entities = []
    for ent_data in data.get("entities", []):
        if ent_data["type"] == "player":
            ent = Player(ent_data["x"], ent_data["y"], ent_data.get("char", "@"))
        elif ent_data["type"] == "monster":
            ent = Monster(ent_data["x"], ent_data["y"], ent_data.get("char", "M"))
        else:
            ent = Entity(ent_data["x"], ent_data["y"], ent_data.get("char", "?"))
        entities.append(ent)
    return tiles, entities


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    tiles, entities = load_level(DEFAULT_LEVEL)
    log = []
    renderer = Renderer(tiles, entities)
    inventory_ui = InventoryUI(stdscr)
    dialogue_ui = DialogueUI(stdscr)
    quest_journal = QuestJournal(stdscr)

    while True:
        stdscr.clear()
        renderer.draw(stdscr)
        # Display player HP and battle log
        player = next(e for e in entities if isinstance(e, Player))
        stdscr.addstr(len(tiles)+1, 0, f"Тимур HP: {player.hp}")
        # Show last 5 log entries
        for idx, entry in enumerate(log[-5:]):
            stdscr.addstr(len(tiles)+2+idx, 0, entry)
        stdscr.refresh()

        key = stdscr.getch()
        if key == -1:
            continue

        if key in (ord("q"), 27):  # quit or ESC
            break
        # Deprecated attack logic removed; use 'c' key for combat

        # Movement keys
        player = next(e for e in entities if isinstance(e, Player))
        dx = dy = 0
        if key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            if key == curses.KEY_UP:
                dy = -1
            elif key == curses.KEY_DOWN:
                dy = 1
            elif key == curses.KEY_LEFT:
                dx = -1
            elif key == curses.KEY_RIGHT:
                dx = 1
            else:
                continue
        elif key == ord("c"):
            # combat attack
            player = next(e for e in entities if isinstance(e, Player))
            for e in list(entities):
                if isinstance(e, Monster) and abs(e.x - player.x) <= 1 and abs(e.y - player.y) <= 1:
                    damage = 5
                    e.hp -= damage
                    log.append(f"Тимур наносит {e.char} {damage} урона")
                    if e.hp <= 0:
                        entities.remove(e)
                        log.append(f"{e.char} побежден")
                        # Clear tile after monster dies
                        row = list(tiles[e.y]); row[e.x] = '.'; tiles[e.y] = ''.join(row)
                    else:
                        damage = 3
                        player.hp -= damage
                        log.append(f"{e.char} наносит Тимуру {damage} урона")
                    break
            continue
        else:
            continue
        new_x = player.x + dx
        new_y = player.y + dy
        # simple bounds check
        if 0 <= new_x < len(tiles[0]) and 0 <= new_y < len(tiles):
            if tiles[new_y][new_x] != "#" and not any(e.x == new_x and e.y == new_y for e in entities):
                player.move(dx, dy)



if __name__ == "__main__":
    curses.wrapper(main)
