import threading
import time

from utils.robot import Robot as CRobot
from utils.robot import RobotSensor as CRobotSensor
from utils.environment import Environment as CEnv

# Environment is global because it exists over anything else
global env

ROBOT_STARTING_POSITION = (0, 0)
ENVIRONMENT_WIDTH = 5
ENVIRONMENT_HEIGHT = 5

def main():
    global env

    # Here we create our Environment before anything else using the global "env" variable
    env = CEnv.Environment((ENVIRONMENT_WIDTH, ENVIRONMENT_HEIGHT))

    # Creating threads
    t_env = threading.Thread(target=start_thread_environment)
    t_robot = threading.Thread(target=start_thread_robot)

    # Starting threads !
    t_env.start()
    t_robot.start()


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

        # Robot explores solutions

        # Robot is in action !

        print(robot.grid)  # Display the grid that robot sees

        # Here is a little delay to see what happens
        time.sleep(1)


def start_thread_environment() -> None:
    global env

    while True:
        # Environment updates himself to add dust or jewel
        env.update_environment()
        # print(env.robot_positions) # Position des robots sur dans la maison
        # Here is a little delay to see what happens
        time.sleep(1)


# Here is the starting point of the app !
if __name__ == '__main__':
    main()
