import sys
import threading
import time
import random

from utils.graphics.Display import Display
from utils.robot import Robot as CRobot
from utils.robot import RobotSensor as CRobotSensor
from utils.environment import Environment as CEnv

# Environment is global because it exists over anything else
global env, display, t_env, t_env_go, t_robot, t_robot_go, t_display, t_display_go

ROBOT_STARTING_POSITION = [0, 0]
ENVIRONMENT_WIDTH = 5
ENVIRONMENT_HEIGHT = 5


def main():
    global env, display, t_env, t_env_go, t_robot, t_robot_go, t_display, t_display_go

    # Create the display window
    display = Display(ENVIRONMENT_WIDTH, ENVIRONMENT_HEIGHT)
    display.create_window()

    # Here we create our Environment before anything else using the global "env" variable
    env = CEnv.Environment((ENVIRONMENT_WIDTH, ENVIRONMENT_HEIGHT), dirty=True)

    # Creating threads
    t_env = threading.Thread(target=start_thread_environment)
    t_robot = threading.Thread(target=start_thread_robot)
    t_display = threading.Thread(target=start_thread_display)

    # Threads can go !!
    t_env_go = True
    t_robot_go = True
    t_display_go = True

    # Starting threads !
    t_env.start()
    t_robot.start()
    t_display.start()

    display.get_window().protocol("WM_DELETE_WINDOW", on_closing)

    # We have to put this line here to be able to update the grid
    display.get_window().mainloop()


def on_closing():
    global display, t_env_go, t_robot_go, t_display_go

    display.get_window().destroy()
    t_env_go = False
    t_robot_go = False
    t_display_go = False


# Here is the robot thread. It is in charge of a single robot living in the environment.
# So starting multiple threads with that function will make multiple robots living in the same environment !
def start_thread_robot() -> None:
    global env, t_robot_go

    # Here we create our robot and his sensor which observes the environment
    sensor = CRobotSensor.RobotSensor(env)
    robot = CRobot.Robot(sensor, ROBOT_STARTING_POSITION)

    while t_robot_go:
        # Robot observes its environment
        robot.observe_environment_with_sensor()

        # Robot updates state bdi

        robot.execute_exploration()

        robot.execute_action_plan()

        # Here is a little delay to see what happens
        time.sleep(1)
        print("r")


def start_thread_environment() -> None:
    global env, t_env_go

    while t_env_go:
        # Environment updates himself to add dust or jewel
        env.update_environment()

        # Here is a little delay to see what happens
        delay = random.randint(5, 10)
        time.sleep(delay)
        print("e")


def start_thread_display() -> None:
    global env, display, t_display_go

    while t_display_go:
        display.update_display(env)
        time.sleep(1)
        print("d")


# Here is the starting point of the app !
if __name__ == '__main__':
    main()
