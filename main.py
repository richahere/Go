import tkinter as tk
from gui import Frame_Board
def main():
	window = tk.Tk()
	window.wm_title("Go AI Game")
	board = Frame_Board(window)
	board.pack()
	window.mainloop()
if __name__ == "__main__":
	main()