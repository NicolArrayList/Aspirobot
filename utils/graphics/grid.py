from tkinter import *
from PIL import Image, ImageTk


def create_grid(event=None):
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    # Creates a vertical line every 100 pixels
    for i in range(0, w, 100):
        canvas.create_line([(i, 0), (i, h)])

    # Creates a horizontal line every 100 pixels
    for i in range(0, h, 100):
        canvas.create_line([(0, i), (w, i)])


# Create an instance of a tkinter frame
window = Tk()

# Set the size of the window
window.geometry("500x500")

# Create a canvas
canvas = Canvas(window, width=500, height=500)
canvas.pack()

canvas.bind('<Configure>', create_grid)

# Loading the image
img = (Image.open("dust-overlay.png"))

# Resizing the image
resized_image = img.resize((80, 80), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized_image)

# Adding image to the canvas
image = canvas.create_image(50, 50, anchor=CENTER, image=new_image)


def move(event):
        if event.char == "q" and canvas.coords(image)[0] != 50:
            canvas.move(image, -100, 0)
        elif event.char == "d" and canvas.coords(image)[0] != 450:
            canvas.move(image, 100, 0)
        elif event.char == "z" and canvas.coords(image)[1] != 50:
            canvas.move(image, 0, -100)
        elif event.char == "s" and canvas.coords(image)[1] != 450:
            canvas.move(image, 0, 100)


window.bind("<Key>", move)
window.resizable(False, False)
window.mainloop()

