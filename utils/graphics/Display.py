from tkinter import *
from PIL import Image, ImageTk
from utils.environment.Environment import Environment
from utils.environment.House import House


class Display:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.window = Tk()
        self.canvas = None

        self.imgAspirobot = ImageTk.PhotoImage(
            (Image.open("utils/graphics/aspirobot.png")).resize((80, 80), Image.ANTIALIAS))
        self.imgDust = ImageTk.PhotoImage((Image.open("utils/graphics/dust.png")).resize((80, 80), Image.ANTIALIAS))
        self.imgDiamonds = ImageTk.PhotoImage(
            (Image.open("utils/graphics/diamonds.png")).resize((80, 80), Image.ANTIALIAS))
        self.imgDustDiamonds = ImageTk.PhotoImage(
            (Image.open("utils/graphics/diamonds_and_dust.png")).resize((80, 80), Image.ANTIALIAS))

        self.grid = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.displayRobot = None

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

        # Call the function to create the grid
        self.canvas.bind('<Configure>', self.create_grid)

        self.window.resizable(False, False)

    def update_display(self, env: Environment):
        house: House = env.house
        posRobot = env.robot_positions[0]

        for i in range(self.width):
            for j in range(self.height):
                self.canvas.delete(self.grid[i][j])
                if house.get_room_at(i, j).has_jewel_and_dust():
                    self.grid[i][j] = self.canvas.create_image(50 + 100 * i, 50 + 100 * j, anchor=CENTER,
                                                               image=self.imgDustDiamonds)
                elif house.get_room_at(i, j).has_jewel():
                    self.grid[i][j] = self.canvas.create_image(50 + 100 * i, 50 + 100 * j, anchor=CENTER,
                                                               image=self.imgDiamonds)
                elif house.get_room_at(i, j).has_dust():
                    self.grid[i][j] = self.canvas.create_image(50 + 100 * i, 50 + 100 * j, anchor=CENTER,
                                                               image=self.imgDust)

        # Display aspirobot here
        self.canvas.delete(self.displayRobot)
        self.displayRobot = self.canvas.create_image(50 + 100 * posRobot[1][0], 50 + 100 * posRobot[1][1], anchor=CENTER,
                                                     image=self.imgAspirobot)

    def get_window(self):
        return self.window