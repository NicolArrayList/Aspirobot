import threading
import time
import random

from utils.graphics.Display import Display
from utils.robot import Robot as CRobot
from utils.robot import RobotSensor as CRobotSensor
from utils.environment import Environment as CEnv

# Environment is global because it exists over anything else
global env, display

ROBOT_STARTING_POSITION = [0, 0]
ENVIRONMENT_WIDTH = 5
ENVIRONMENT_HEIGHT = 5

def main():
    global env, display

    # Create the display window
    display = Display(ENVIRONMENT_WIDTH, ENVIRONMENT_HEIGHT)
    display.create_window()

    # Here we create our Environment before anything else using the global "env" variable
    env = CEnv.Environment((ENVIRONMENT_WIDTH, ENVIRONMENT_HEIGHT), dirty=True)

    # Creating threads
    t_env = threading.Thread(target=start_thread_environment)
    t_robot = threading.Thread(target=start_thread_robot)
    t_display = threading.Thread(target=start_thread_display)

    # Starting threads !
    t_env.start()
    t_robot.start()
    t_display.start()

    # We have to put this line here to be able to update the grid
    display.get_window().mainloop()


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

        # Here is a little delay to see what happens
        delay = random.randint(5, 10)
        time.sleep(delay)


def start_thread_display() -> None:
    global env, display

    while True:
        display.update_display(env)
        time.sleep(1)


# Here is the starting point of the app !
if __name__ == '__main__':
    main()