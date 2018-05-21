import time
import curses
from screens import HistoryScreen

class CursesScreen(HistoryScreen):
    def __init__(self, win, blink_period=0.200, history=100, ratio=0.5):
        y, x = win.getmaxyx()
        self.win = win
        self.blink_period = blink_period
        self.blink_start = time.time()
        self.blink_state = True
        super(HistoryScreen, self).__init__(x, y, history, ratio)

    def redraw(self):
        for  i, d in enumerate(self.display):
            self.win.insstr(i, 0, d)

        wy = self.cursor.y
        wx = self.cursor.x

        try:
            if ((time.time()-self.blink_start)>self.blink_period):
                self.blink_start = time.time()
                if self.blink_state:
                    self.win.chgat(wy, wx, 1, curses.A_STANDOUT)
                else:
                    self.win.chgat(wy, wx, 1, curses.A_NORMAL)
                self.blink_state = not self.blink_state
        except:
            pass

        self.win.redrawwin()
        self.win.noutrefresh()
