"""Dialogue UI.

Displays a simple multiline dialogue box.
"""

import curses
from textwrap import wrap


class DialogueUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def show(self, text: str):
        h, w = self.stdscr.getmaxyx()
        win = curses.newwin(h//2, w-4, h//4, 2)
        win.clear()
        win.border()
        win.addstr(1, 2, "Dialogue")
        lines = wrap(text, w-6)
        for idx, line in enumerate(lines, start=3):
            win.addstr(idx, 4, line)
        win.addstr(h//2-2, 2, "Press any key to continue")
        win.refresh()
        win.getch()
