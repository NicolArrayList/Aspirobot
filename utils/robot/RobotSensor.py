from utils.environment import Environment as CEnv


class RobotSensor:
    def __init__(self, environment_to_track: 'CEnv.Environment'):
        self.tracked_environment = environment_to_track

    def read_environment(self):
        return self.tracked_environment.house
