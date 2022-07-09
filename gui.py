import tkinter as tk
import math
from game import Game
class Canvas(tk.Canvas):
    def __init__(self, master=None, height=0, width=0):
        tk.Canvas.__init__(self, master, height=height, width=width, background='#dd88ff')
        self.draw_board()
        self.game = Game()
    def draw_board(self):
        for i in range(1, 16):
            start_pixel_x = i * 30
            start_pixel_y = 30
            end_pixel_x = i * 30
            end_pixel_y = 450
            self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)
        for i in range(1,16):
            start_pixel_x = 30
            start_pixel_y = i * 30
            end_pixel_x = 450
            end_pixel_y = i * 30
            self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)
    def draw_piece(self, row, col):
        start_pixel_x = (row + 1) * 30 - 13
        start_pixel_y = (col + 1) * 30 - 13
        end_pixel_x = (row + 1) * 30 + 13
        end_pixel_y = (col + 1) * 30 + 13
        if self.game.turn() == 1:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='yellow')

        elif self.game.turn() == 2:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')
    def go_game(self, event):
        while True:
            invalid_pos = True
            for i in range(self.game.size()):
                for j in range(self.game.size()):
                    pixel_x = (i + 1) * 30
                    pixel_y = (j + 1) * 30
                    square_x = math.pow((event.x - pixel_x), 2)
                    square_y = math.pow((event.y - pixel_y), 2)
                    distance =  math.sqrt(square_x + square_y)
                    boundary = math.sqrt(2) * self.game.size()
                    if (distance < boundary and (self.game.board()[i][j] == 0)):
                        invalid_pos = False
                        row, col = i, j
                        self.draw_piece(i,j)
                        break	
                else:
                    continue
                break			
            if invalid_pos:
                print('Invalid position.\n')
                break
            break
        self.game.make_move(row,col)
        self.unbind('<Button-1>')
        if self.game.check() == 2:
            self.create_text(250, 450, text = 'You Win!')
            self.unbind('<Button-1>')
            return 0
        val = self.game.choose_move()
        row = val.get('choice')[0]
        col = val.get('choice')[1]
        self.draw_piece(row,col)
        self.game.make_move(row,col)
        self.bind('<Button-1>', self.go_game)
        if self.game.check() == 1:
            self.create_text(250, 475, text = 'AI wins!')
            self.unbind('<Button-1>')
            return 0
class Frame_Board(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.create_widgets()
    def create_widgets(self):
        self.Canvas = Canvas(height = 500, width = 500)
        self.Canvas.bind('<Button-1>', self.Canvas.go_game)
        self.Canvas.pack()
