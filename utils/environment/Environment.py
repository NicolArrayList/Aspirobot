import copy
import random

from utils.environment.House import House
from utils.robot import Robot as CRobot


class Environment:
    def __init__(self, env_size: (int, int)):
        self.__size = env_size
        self.__width = self.__size[0]
        self.__height = self.__size[1]
        self.__house = House(self.__width, self.__height)
        self.__robot_positions = []

    def update_environment(self):
        # JUST AN EXAMPLE
        position_x = random.randrange(self.__height)
        position_y = random.randrange(self.__width)
        # self.__house[position_x][position_y] = [True, True]

    def set_dust_room(self, room_position: (int, int), set_dust: bool) -> None:
        self.__house.get_room_at(room_position[0], room_position[1]).set_dust_room(set_dust)

    def set_jewel_room(self, room_position: (int, int), set_jewel: bool) -> None:
        self.__house.get_room_at(room_position[0], room_position[1]).set_jewel_room(set_jewel)

    def update_robot_positions(self, robot: 'CRobot.Robot', position: list[int]):
        for it_robot in self.__robot_positions:
            if robot == (it_robot[0]):
                it_robot[1] = position
                return
        self.__robot_positions.append([robot, position])

    @property
    def house(self) -> House:
        return copy.deepcopy(self.__house)

    @property
    def robot_positions(self) -> list['CRobot.Robot']:
        return copy.deepcopy(self.__robot_positions)
