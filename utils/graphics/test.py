from utils.graphics.Display import Display

display = Display(5, 5)
display.create_window()
display.test_image(0, 3)

# We have to put this line here to be able to update the grid
display.get_window().mainloop()
