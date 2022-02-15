import time
from math import sqrt

from utils.environment.House import House
from utils.node.Node import Node

from utils.robot.RobotSensor import RobotSensor
from utils.robot.RobotActuator import RobotActuator

from utils.environment.Room import Room


class Robot:
    def __init__(self, sensor: RobotSensor, starting_position: list[int],
                 max_depth: int = 5, max_iteration_before_informed_search: int = 5):
        self.robotSensor = sensor
        self.robotActuator = RobotActuator(sensor.tracked_environment)
        self.house: House = None

        self.position = starting_position
        self.action_plan = []

        self.robotActuator.robot_move(self, self.position)

        # UNINFORMED PARAMETERS
        self.max_depth = max_depth

        self.vacuumedDust = 0
        self.collectedDiamonds = 0
        self.vacuumedDiamonds = 0

        self.nbIterations = 0
        self.maxIteration = max_iteration_before_informed_search

        self.metric = 99

    def observe_environment_with_sensor(self) -> None:
        self.house = self.robotSensor.read_environment()
        self.position = self.robotSensor.get_robot_position_in_environment(self)

    def execute_exploration(self) -> None:

        closest_target_room = self.get_closest_target()

        if closest_target_room is None:
            self.action_plan = [self.position]
        else:
            if self.nbIterations < self.maxIteration:
                self.action_plan = self.__depth_limited_search()
            else:
                self.action_plan = self.__astar(closest_target_room.get_room_position())

            
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
                        shortest_distance = self.distance_to_room(current_room)
                        self.metric = sqrt(shortest_distance)

        return closest_target

    def distance_to_room(self, room: Room) -> float:
        room_pos = room.get_room_position()
        # Euclidian distance without square root because distance order is conserved (with positive int)
        return ((room_pos[0] - self.position[0]) ** 2) + ((room_pos[1] - self.position[1]) ** 2)

    """
    Method to start a recursive Depth Limited Search 
    -> this method start an iterative depth exploration calling  __deep_limited_search_it()
    -> maximum depth of exploration is set by attribute max_depth of the robot
    """
    def __depth_limited_search(self):
        visited_nodes = set()

        start_node = Node(None, self.position)

        action_plan = self.__depth_limited_search_it(start_node, visited_nodes, 0)

        return action_plan[::-1]

    """
    Method to do an iteration of Depth Limited Search 
    -> this method looks at the neighbouring nodes and call itself recursively to complete exploration
    -> depth parameter is the current depth of exploration
    -> visited_nodes is used to avoid nodes we already went in 
    """

    def __depth_limited_search_it(self, current_node, visited_nodes, depth):
        # Make sure not to overpass the max depth
        if depth >= self.max_depth:
            return None

        # Make sure the node is a new node
        if current_node not in visited_nodes:
            visited_nodes.add(current_node)

            # Each neighbouring room are cases we can explore ( DOWN | UP | RIGHT | LEFT )
            for new_position in [(0, 1), (0, -1), (1, 0), (-1, 0)]:

                # Here is the node's position we will explore next
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure that it's in our environment range, if not skip it
                if \
                        node_position[0] > (self.house.get_width() - 1) or \
                        node_position[1] > (self.house.get_height() - 1) or \
                        node_position[0] < 0 or \
                        node_position[1] < 0:
                    continue

                # Now everything is alright for this node to exist, we create it
                new_node = Node(current_node, node_position)

                # If the node contains dust or jewel : it's our objective, so we return it
                if self.house.get_room_at(node_position[0], node_position[1]).has_jewel_or_dust():
                    return [node_position, current_node.position]

                # If it's empty : we recursively call the function to explore what's next to this node
                else:
                    result_of_search = self.__depth_limited_search_it(new_node, visited_nodes, depth + 1)

                    # Here exploration found something, so we return our node to build the path to our objective
                    if result_of_search is not None:
                        result_of_search.append(current_node.position)
                        return result_of_search
                    # If this branch of exploration returns None, it means that we haven't found anything to do on it

            # If we reach this point, it means that there is no more options for this branch
            return None

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

    def get_metric(self):
        return self.metric
