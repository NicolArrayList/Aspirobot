import time

from utils.environment.House import House
from utils.node.Node import Node

from utils.robot.RobotSensor import RobotSensor
from utils.robot.RobotActuator import RobotActuator

from utils.environment.Room import Room


class Robot:
    def __init__(self, sensor: RobotSensor, starting_position: list[int]):
        self.robotSensor = sensor
        self.robotActuator = RobotActuator(sensor.tracked_environment)
        self.house: House = None

        self.position = starting_position
        self.action_plan = []

        self.robotActuator.robot_move(self, self.position)

        self.vacuumedDust = 0
        self.collectedDiamonds = 0
        self.vacuumedDiamonds = 0

        self.nbIterations = 0

    def observe_environment_with_sensor(self) -> None:
        self.house = self.robotSensor.read_environment()
        self.position = self.robotSensor.get_robot_position_in_environment(self)

    def execute_exploration(self) -> None:
        closest_target_room = self.get_closest_target()

        if closest_target_room is not None:
            self.action_plan = self.__astar(closest_target_room.get_room_position())
        else:
            self.action_plan = [self.position]


    def execute_action_plan(self):
        for position in self.action_plan:
            self.robotActuator.robot_move(self, position)
            time.sleep(2)

        self.position = self.robotSensor.get_robot_position_in_environment(self)

        if self.house.get_room_at(self.position[0], self.position[1]).has_dust():
            self.robotActuator.aspire(self.position)
            self.vacuumedDust += 1
            if self.house.get_room_at(self.position[0], self.position[1]).has_jewel():
                self.vacuumedDiamonds += 1
        elif self.house.get_room_at(self.position[0], self.position[1]).has_jewel():
            self.robotActuator.collect(self.position)
            self.collectedDiamonds += 1

        self.nbIterations += 1

    def get_closest_target(self) -> Room:
        closest_target = None
        for x in range(self.house.get_width()):
            for y in range(self.house.get_height()):
                if self.house.get_room_at(x, y).has_jewel_or_dust():
                    current_room = self.house.get_room_at(x, y)
                    if closest_target is None:
                        closest_target = current_room
                    elif self.distance_to_room(current_room) <= self.distance_to_room(closest_target):
                        closest_target = current_room
        return closest_target

    def distance_to_room(self, room: Room) -> float:
        room_pos = room.get_room_position()
        # Euclidian distance without square root because distance order is conserved (with positive int)
        return ((room_pos[0] - self.position[0]) ** 2) + ((room_pos[1] - self.position[1]) ** 2)

    def __astar(self, end_position):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        # F is the total cost of the node.
        # G is the distance between the current node and the start node.
        # H is the heuristic — estimated distance from the current node to the end node.

        # Getting start
        start_position = self.position

        # Creating nodes
        start_node = Node(None, start_position)
        # start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end_position)
        # end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        # closed_list is useless with a distance metric to get to a unique position
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if \
                        node_position[0] > (self.house.get_width() - 1) or \
                                node_position[1] > (self.house.get_height() - 1) or \
                                node_position[0] < 0 or \
                                node_position[1] < 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + \
                          ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

    def get_action_plan(self):
        return self.action_plan

    def get_vacuumed_dust(self):
        return self.vacuumedDust

    def get_collected_diamonds(self):
        return self.collectedDiamonds

    def get_vacuumed_diamonds(self):
        return self.vacuumedDiamonds

    def get_nb_iterations(self):
        return self.nbIterations
