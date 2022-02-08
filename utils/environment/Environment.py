import copy
import random

from utils.robot import Robot as CRobot


class Environment:
    def __init__(self, env_size: (int, int)):
        self.__size = env_size
        self.__width = self.__size[0]
        self.__height = self.__size[1]
        self.__grid = [[[False, False] for i in range(0, self.__width)] for j in range(0, self.__height)]
        self.__robot_positions = set()

    def update_environment(self):
        # JUST AN EXAMPLE
        position_x = random.randrange(self.__height)
        position_y = random.randrange(self.__width)
        self.__grid[position_x][position_y] = [True, True]

    def set_dust_room(self, room_position: (int, int), sets: bool) -> None:
        self.__grid[room_position[0]][room_position[1]][0] = sets

    def set_jewel_room(self, room_position: (int, int), sets: bool) -> None:
        self.__grid[room_position[0]][room_position[1]][1] = sets

    def update_robot_positions(self, robot: 'CRobot.Robot', position: list[int]):
        for ID, val in enumerate(self.__robot_positions):
            if robot == (val[0]):
                val[1] = position
                return
        self.__robot_positions.add((robot, position))

    @property
    def grid(self) -> list[list[list[bool]]]:
        return copy.deepcopy(self.__grid)

    @property
    def robot_positions(self) -> set:
        return copy.deepcopy(self.__robot_positions)
