from utils.environment import Environment as CEnv


class RobotSensor:
    def __init__(self, environment_to_track: 'CEnv.Environment'):
        self.tracked_environment = environment_to_track

    def read_environment(self):
        return self.tracked_environment.house

    def get_robot_position_in_environment(self, robot):
        return self.tracked_environment.get_robot_position(robot)
