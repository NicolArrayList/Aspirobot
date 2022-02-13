from utils.environment.Room import Room


class House:
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__grid = [[Room(i, j) for j in range(0, self.__width)] for i in range(0, self.__height)]

    def get_room_at(self, position_x: int, position_y: int) -> Room:
        return self.__grid[position_x][position_y]

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def __str__(self):
        for i in range(self.__width):
            print(self.__grid[i] + "\n")
