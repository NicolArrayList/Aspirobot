from utils.graphics.Display import Display

display = Display(5, 5)
display.create_window()
display.update_display()

# We have to put this line here to be able to update the grid
display.get_window().mainloop()