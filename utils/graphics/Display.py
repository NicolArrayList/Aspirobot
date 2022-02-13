from tkinter import *
from PIL import Image, ImageTk


class Display:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.window = Tk()
        self.canvas = None

        self.imgAspirobot = ImageTk.PhotoImage((Image.open("aspirobot.png")).resize((80, 80), Image.ANTIALIAS))
        self.imgDust = ImageTk.PhotoImage((Image.open("dust.png")).resize((80, 80), Image.ANTIALIAS))
        self.imgDiamonds = ImageTk.PhotoImage((Image.open("diamonds.png")).resize((80, 80), Image.ANTIALIAS))
        self.imgDustDiamonds = ImageTk.PhotoImage(
            (Image.open("diamonds_and_dust.png")).resize((80, 80), Image.ANTIALIAS))

        self.grid = [[0 for _ in range(self.height)] for _ in range(self.width)]

    def create_grid(self, event=None):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # Creates a vertical line every 100 pixels
        for i in range(0, w, 100):
            self.canvas.create_line([(i, 0), (i, h)])

        # Creates a horizontal line every 100 pixels
        for i in range(0, h, 100):
            self.canvas.create_line([(0, i), (w, i)])

    def create_window(self):
        # Set the size of the window
        self.window.geometry(str(self.width) + "00x" + str(self.height) + "00")

        # Create a canvas
        self.canvas = Canvas(self.window, width=self.width * 100, height=self.height * 100)
        self.canvas.pack()

        self.canvas.bind('<Configure>', self.create_grid)

        self.window.resizable(False, False)

    def update_display(self):
        for i in range(self.width):
            for j in range(self.height):
                self.canvas.delete(self.grid[i][j])
                # Check the house rooms here
                self.grid[i][j] = self.canvas.create_image(50 + 100 * i, 50 + 100 * j, anchor=CENTER, image=self.imgAspirobot)

    def get_window(self):
        return self.window
