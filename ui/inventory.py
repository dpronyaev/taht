"""Inventory UI.

Shows a simple list of items held by the player.
"""

import curses
from typing import List


class InventoryUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def show(self, entities):
        # Find player inventory
        player = next(e for e in entities if hasattr(e, "inventory"))
        items = player.inventory
        h, w = self.stdscr.getmaxyx()
        win = curses.newwin(h, w, 0, 0)
        win.clear()
        win.border()
        win.addstr(1, 2, "Inventory")
        for idx, item in enumerate(items, start=3):
            win.addstr(idx, 4, f"- {item}")
        win.addstr(h-2, 2, "Press any key to close")
        win.refresh()
        win.getch()
