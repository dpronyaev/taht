"""Quest journal UI.

Shows a static list of quests (for now).  This can be expanded to
track status, objectives, etc.
"""

import curses


class QuestJournal:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def show(self):
        h, w = self.stdscr.getmaxyx()
        win = curses.newwin(h, w, 0, 0)
        win.clear()
        win.border()
        win.addstr(1, 2, "Quest Journal")
        win.addstr(3, 4, "- Find the hidden key to open the great hall")
        win.addstr(4, 4, "- Defeat the guard at the gate")
        win.addstr(h-2, 2, "Press any key to close")
        win.refresh()
        win.getch()
