import threading

def main():

    t_Env = threading.Thread(startThreadEnvironment)
    t_Robot = threading.Thread(startThreadRobot)


    t_Env.start()
    t_Robot.start()

def startThreadRobot():
    while True :


def startThreadEnvironment():
    while True :



main()