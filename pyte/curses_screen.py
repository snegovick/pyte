import time
import curses
from .screens import Screen, HistoryScreen
from wcwidth import wcwidth

class CursesScreen(Screen):
    def __init__(self, win, blink_period=.2, history=100, ratio=.5):
        y, x = win.getmaxyx()
        self.win = win
        self.blink_period = blink_period
        self.blink_start = time.time()
        self.blink_state = True
        #super(CursesScreen, self).__init__(x, y, history=history, ratio=ratio)
        super(CursesScreen, self).__init__(x, y)#, history=history, ratio=ratio)

    def redraw(self):

        for y in range(self.lines):
            is_wide_char = False
            attrs = []
            disp_line = ''
            line = self.buffer[y]
            for x in range(self.columns):
                if is_wide_char:  # Skip stub
                    is_wide_char = False
                    continue
                char = line[x].data
                if line[x].reverse:
                    if ((len(attrs)>0) and (attrs[-1][1]==(x-1))):
                        attrs[-1][2]+=1
                    else:
                        attrs.append([y, x, 1, curses.A_REVERSE])
                assert sum(map(wcwidth, char[1:])) == 0
                is_wide_char = wcwidth(char[0]) == 2
                disp_line += char

            self.win.insstr(y, 0, disp_line)
            for a in attrs:
                self.win.chgat(a[0], a[1], a[2], a[3])

        wy = self.cursor.y
        wx = self.cursor.x

        try:
            if ((time.time()-self.blink_start)>self.blink_period):
                if self.blink_state:
                    self.blink_state = False
                    self.win.chgat(wy, wx, 1, curses.A_STANDOUT)
                else:
                    self.blink_state = True
                    self.win.chgat(wy, wx, 1, curses.A_NORMAL)
                self.blink_start = time.time()
            if self.blink_state:
                self.win.chgat(wy, wx, 1, curses.A_STANDOUT)
            else:
                self.win.chgat(wy, wx, 1, curses.A_NORMAL)

        except:
            pass

        self.win.redrawwin()
        self.win.noutrefresh()
