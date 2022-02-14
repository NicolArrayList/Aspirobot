from utils.robot import Robot as CRobot
from utils.environment import Environment as CEnv


class RobotActuator:
    def __init__(self, environment_to_actualize: 'CEnv.Environment'):
        self.env = environment_to_actualize

    def aspire(self, position: list[int]) -> None:
        self.env.set_dust_room(position, False)
        self.env.set_jewel_room(position, False)

    def collect(self, position: list[int]) -> None:
        self.env.set_jewel_room(position, False)

    def robot_move(self, robot: 'CRobot.Robot', position: list[int]) -> None:
        self.env.update_robot_positions(robot, position)
