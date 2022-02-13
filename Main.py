import threading
import time
import random

from utils.robot import Robot as CRobot
from utils.robot import RobotSensor as CRobotSensor
from utils.environment import Environment as CEnv

# Environment is global because it exists over anything else
global env

ROBOT_STARTING_POSITION = [0, 0]
ENVIRONMENT_WIDTH = 5
ENVIRONMENT_HEIGHT = 5

def main():
    global env

    # Here we create our Environment before anything else using the global "env" variable
    env = CEnv.Environment(env_size=(ENVIRONMENT_WIDTH, ENVIRONMENT_HEIGHT), dirty=True)

    # Creating threads
    t_env = threading.Thread(target=start_thread_environment)
    t_robot = threading.Thread(target=start_thread_robot)

    # Starting threads !
    t_env.start()
    t_robot.start()


""" pour le a_star
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (7, 6)

    path = astar(maze, start, end)
    print(path)
"""


# Here is the robot thread. It is in charge of a single robot living in the environment.
# So starting multiple threads with that function will make multiple robots living in the same environment !
def start_thread_robot() -> None:
    global env

    # Here we create our robot and his sensor which observes the environment
    sensor = CRobotSensor.RobotSensor(env)
    robot = CRobot.Robot(sensor, ROBOT_STARTING_POSITION)

    while True:
        # Robot observes its environment
        robot.observe_environment_with_sensor()

        # Robot updates state bdi

        robot.execute_exploration()

        robot.execute_action_plan()

        # Here is a little delay to see what happens
        time.sleep(1)


def start_thread_environment() -> None:
    global env

    while True:
        # Environment updates himself to add dust or jewel
        env.update_environment()
        # print(env.robot_positions) # Position des robots sur dans la maison
        # Here is a little random delay to see what happens
        delay = random.randint(10, 20)

        time.sleep(delay)


# Here is the starting point of the app !
if __name__ == '__main__':
    main()
