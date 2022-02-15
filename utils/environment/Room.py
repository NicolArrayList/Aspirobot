from typing import Tuple


class Room:
    def __init__(self, position_x: int, position_y: int, dust=False, jewel=False):
        self.__posX = position_x
        self.__posY = position_y
        self.__dust = dust
        self.__jewel = jewel

    def get_room_position(self) -> tuple:
        return self.__posX, self.__posY

    def set_dust_room(self, set_dust_to: bool) -> None:
        self.__dust = set_dust_to

    def set_jewel_room(self, set_jewel_to: bool) -> None:
        self.__jewel = set_jewel_to

    def has_jewel_or_dust(self):
        return self.has_jewel() or self.has_dust()

    def has_jewel_and_dust(self):
        return self.has_jewel() and self.has_dust()

    def has_jewel(self):
        return self.__jewel

    def has_dust(self):
        return self.__dust
