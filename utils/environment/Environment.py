import copy
import random

from utils.environment.House import House
from utils.robot import Robot as CRobot


class Environment:
    def __init__(self, env_size: (int, int), dirty: bool = False):
        self.__size = env_size
        self.__width = self.__size[0]
        self.__height = self.__size[1]
        self.__house = House(self.__width, self.__height)
        self.__robot_positions = []

        # Randomly sets room with dust or jewel based on the dirty argument
        if dirty:
            dirty_random = random.randint(4, 6)
            for i in range(dirty_random):
                self.update_environment()

    """
    This method uses random numbers to find a room and put dust or jewel in it
    """
    def update_environment(self):
        # find a random room
        position_x = random.randrange(self.__height)
        position_y = random.randrange(self.__width)

        # find out what dust or jewellery will be in the room
        heads_or_tails = bool(random.getrandbits(1))

        if heads_or_tails:
            self.set_dust_room((position_x, position_y), True)
        else:
            self.set_jewel_room((position_x, position_y), True)

    def set_dust_room(self, room_position: (int, int), set_dust: bool) -> None:
        self.__house.get_room_at(room_position[0], room_position[1]).set_dust_room(set_dust)

    def set_jewel_room(self, room_position: (int, int), set_jewel: bool) -> None:
        self.__house.get_room_at(room_position[0], room_position[1]).set_jewel_room(set_jewel)

    """
    IMPORTANT : This method has been designed to support multiple robots, which is not yet the case
    """
    def update_robot_positions(self, robot: 'CRobot.Robot', position: list[int]) -> None:
        for it_robot in self.__robot_positions:
            if robot == (it_robot[0]):
                it_robot[1] = position
                return
        self.__robot_positions.append([robot, position])

    def get_robot_position(self, robot: 'CRobot.Robot') -> [list[int], None]:
        for it_robot in self.__robot_positions:
            if robot == (it_robot[0]):
                return it_robot[1]
        return None

    @property
    def house(self) -> House:
        return copy.deepcopy(self.__house)

    @property
    def robot_positions(self) -> list['CRobot.Robot']:
        return copy.deepcopy(self.__robot_positions)

    def __str__(self):
        tab = ''
        for x in range(self.__width):
            for y in range(self.__height):

                for i in range(len(self.robot_positions)):
                    if self.robot_positions[i][1] == (x, y):
                        tab += "R"

                if self.__house.get_room_at(x, y).has_dust():
                    tab += "d "
                elif self.__house.get_room_at(x, y).has_jewel():
                    tab += "j "
                else:
                    tab += "x "
            tab += "\n"
        return tab
