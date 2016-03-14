# -*- coding: utf-8 -*-

# author : Hun Min Park
# last modified : 2016.03.14

import Tkinter as tk
from math import sin, cos, tan, pi

title = 'ArchiPi'
poly_min = 5
poly_max = 500

class PiApp(object):
    ''' appplication design '''
    def __init__(self,
                 board_size = (300, 300),
                 board_margin = 10,
                 radius = 100,
                 color_background = 'white',
                 color_circle = 'gray',
                 color_polygon_in = 'gray',
                 color_polygon_out = 'gray'):
        ''' class initialization '''
        self.root = tk.Tk()
        self.root.wm_title(title)
        self.root.protocol('WM_DELETE_WINDOW', self.quit)

        self.w, self.h = board_size
        self.m = board_margin
        self.r = radius
        self.color = {
            'bg' : color_background,
            'circle' : color_circle,
            'poly_in' : color_polygon_in,
            'poly_out' : color_polygon_out
        }

        self.draw_frames()
        self.draw_board()
        self.draw_status()
        self.draw_entry()
        self.draw_control()

    # -------------------------------------------

    def draw_frames(self):
        ''' design the frames
        [Structure]
        ----- main --------------
        | - board - - display - |
        | |       | | status  | |
        | | (...) | | entry   | |
        | |       | | control | |
        | --------- ----------- |
        -------------------------
        '''
        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(padx = 10, pady = 10)

        self.frame_board = tk.Frame(self.frame_main)
        self.frame_display = tk.Frame(
            self.frame_main,
            borderwidth = 2,
            relief = tk.RIDGE
        )

        self.frame_board.grid(row = 0, column = 0)
        self.frame_display.grid(row = 0, column = 1)
        
        self.frame_status = tk.Frame(
            self.frame_display,
            borderwidth = 2,
            relief = tk.GROOVE
        )
        self.frame_entry = tk.Frame(self.frame_display)
        self.frame_control = tk.Frame(self.frame_display)

        self.frame_status.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.frame_entry.grid(row = 1, column = 0, padx = 5, pady = 8)
        self.frame_control.grid(row = 2, column = 0, padx = 5, pady = 5)
    
    def draw_board(self):
        ''' draw the board (= canvas object) and
        the background / the circle
        '''
        self.board = tk.Canvas(
            self.frame_board,
            width = self.w + self.m*2,
            height = self.h + self.m*2
        )
        self.board.pack()

        self.bg = self.board.create_rectangle(
            self.m,
            self.m,
            self.w + self.m,
            self.h + self.m,
            fill = self.color['bg'],
            tags = 'bg'
        )

        self._draw_circle(self.r, self.color['circle'])

    def draw_status(self):
        ''' draw a label which displays the result
        of calculation
        '''
        self.label_pi = tk.Label(
            self.frame_status,
            text = '',
            justify = tk.LEFT
        )
        self.label_pi.pack(padx = 5, pady = 5)

        self._update_status(0, 0, 0)

    def draw_entry(self):
        ''' draw an entry for getting an input '''
        self.label_poly = tk.Label(
            self.frame_entry,
            text = 'Number of sides :\n'\
            '(between %d - %d)' % (poly_min, poly_max)
        )
        self.label_poly.grid(row = 0, column = 0, pady = 2)

        self.n_input = tk.StringVar()
        self.n_input.trace('w', self._callback_entry)

        self.n_len = len(str(poly_max))

        self.entry_poly = tk.Entry(
            self.frame_entry,
            textvariable = self.n_input,
            width = 7
        )
        self.entry_poly.grid(row = 1, column = 0, pady = 2)

    def draw_control(self):
        ''' draw a control board (= buttons) '''
        self.button_run = tk.Button(
            self.frame_control,
            text = 'Run',
            command = self.do_job
        )
        self.button_quit = tk.Button(
            self.frame_control,
            text = 'Quit',
            command = self.quit
        )

        self.button_run.grid(row = 0, column = 0, pady = 2)
        self.button_quit.grid(row = 1, column = 0, pady = 2)

    # -------------------------------------------

    def _update_status(self, area_in, area_out, pi_est):
        ''' internal function : update self.label_poly '''
        self.label_pi.configure(
            text = 'Area of polygon (inside)\n'\
            ': %.5f\n'\
            'Area of polygon (outside)\n'\
            ': %.5f\n'\
            'Estimated value of pi\n'\
            ': %.12f' % (area_in, area_out, pi_est),
        )

    def _callback_entry(self, *dummy):
        ''' internal function : limit the length of input '''
        n_old = self.n_input.get()

        if len(n_old) > self.n_len:
            n_new = n_old[:len(str(poly_max))]
            self.n_input.set(n_new)

    def _draw_circle(self, radius, color):
        ''' internal function : helper function for
        drawing a circle '''
        self.board.create_oval(
            self.m + self.w/2 - radius,
            self.m + self.h/2 - radius,
            self.m + self.w/2 + radius,
            self.m + self.h/2 + radius,
            fill = color,
            tags = 'circle'
        )


    def _draw_polygon(self, num_sides, radius, color):
        ''' internal function : helper function for
        drawing a polygon '''
        angle = (2*pi)/num_sides
        x0, y0 = self.m + self.w/2, self.m + self.h/2
        points = []

        for i in xrange(num_sides):
            points.append(x0 + radius*cos(i*angle))
            points.append(y0 + radius*sin(i*angle))

        self.board.create_polygon(
            *points,
            fill = color,
            outline = 'black',
            tags = 'poly'
        )

    def _draw_lines(self, num_sides, radius, color):
        ''' internal function : helper function for
        drawing lines from the center to each vertex
        '''
        angle = (2*pi)/num_sides
        x0, y0 = self.m + self.w/2, self.m + self.h/2

        for i in xrange(num_sides):
            self.board.create_line(
                x0,
                y0,
                x0 + radius*cos(i*angle),
                y0 + radius*sin(i*angle),
                fill = color,
                tags = 'line'
            )

    # -------------------------------------------

    def do_job(self):
        ''' mainloop of calculation '''
        # get the input
        n_input = self.entry_poly.get()
        
        # if the input is wrong (not int / not in the range),
        # then just ignore it and do nothing
        if not n_input.isdigit():
            return
        
        n = int(n_input)

        if n < poly_min or n > poly_max:
            return

        # calculate the radius
        r_circle = self.r
        r_poly_in = self.r
        r_poly_out = self.r/cos(pi/n)

        # clear the board
        self.board.delete('circle')
        self.board.delete('poly')
        self.board.delete('line')

        # draw the polygon (outside)
        self._draw_polygon(n, r_poly_out, self.color['poly_out'])

        # draw the circle
        self._draw_circle(r_circle, self.color['circle'])

        # draw the polygon (inside)
        self._draw_polygon(n, r_poly_in, self.color['poly_in'])

        # draw the lines from the center to each vertex
        self._draw_lines(n, r_poly_out, 'black')

        # estimate the value of pi
        _area_in = (n*r_poly_in*r_poly_in*sin((2*pi)/n))/2
        _area_out = (n*r_poly_out*r_poly_out*sin((2*pi)/n))/2
        _pi_est = (_area_in + _area_out)/(2*r_circle*r_circle)

        # update the result on the screen
        self._update_status(
            area_in = _area_in,
            area_out = _area_out,
            pi_est = _pi_est
        )

    # -------------------------------------------

    def run(self):
        ''' start the app '''
        self.root.mainloop()

    def quit(self):
        ''' quit the app '''
        self.root.destroy()

if __name__ == '__main__':
    app = PiApp(
        board_size = (300, 300),
        radius = 110,
        color_circle = 'yellow',
        color_polygon_in = 'lawn green',
        color_polygon_out = 'cyan'
    )

    app.run()
