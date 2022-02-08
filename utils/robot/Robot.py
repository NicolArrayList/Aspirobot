from utils.robot.RobotSensor import RobotSensor
from utils.robot.RobotActuator import RobotActuator


class Robot:
    def __init__(self, sensor: RobotSensor, starting_position: (int, int)):
        self.position = starting_position
        self.robotSensor = sensor
        self.robotActuator = RobotActuator(sensor.tracked_environment)
        self.grid = None

        self.robotActuator.robot_move(self, self.position)

    def observe_environment_with_sensor(self) -> None:
        self.grid = self.robotSensor.read_environment()
