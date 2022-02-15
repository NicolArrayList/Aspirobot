class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, depth=None):
        # Parent node
        self.parent = parent
        # Position associated
        self.position = position
        # Depth in the current branch
        self.depth = depth

        # F is the total cost of the node.
        # G is the distance between the current node and the start node.
        # H is the heuristic — estimated distance from the current node to the end node.
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position[0]) + hash(self.position[1])
