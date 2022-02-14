from tkinter import *
from PIL import Image, ImageTk
from utils.environment.Environment import Environment
from utils.environment.House import House
from utils.robot.Robot import Robot


class Display:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.window = Tk()
        self.window.wm_title("Aspirobot")

        self.canvas = None

        # Images to represent the environment
        self.imgAspirobot = ImageTk.PhotoImage(
            (Image.open("utils/graphics/aspirobot.png")).resize((80, 80), Image.ANTIALIAS))
        self.imgDust = ImageTk.PhotoImage((Image.open("utils/graphics/dust.png")).resize((80, 80), Image.ANTIALIAS))
        self.imgDiamonds = ImageTk.PhotoImage(
            (Image.open("utils/graphics/diamonds.png")).resize((80, 80), Image.ANTIALIAS))
        self.imgDustDiamonds = ImageTk.PhotoImage(
            (Image.open("utils/graphics/diamonds_and_dust.png")).resize((80, 80), Image.ANTIALIAS))

        # Displayed elements
        self.grid = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.displayRobot = None

        self.displayExploration = None
        self.displayIterations = None

        self.displayPlan = None
        self.displayGoal = None

        self.displayMetric = None
        self.metricValue = 0

        self.displayVacuumedDust = None
        self.displayCollectedDiamonds = None
        self.displayVacuumedDiamonds = None

        # Graphic elements
        self.line1 = None

    # Creates the lines of the grid
    def create_grid(self, event=None):
        w = 100 * self.width + 1
        h = 100 * self.height + 1

        # Creates a vertical line every 100 pixels
        for i in range(0, w, 100):
            self.canvas.create_line([(i, 0), (i, h)])

        # Creates a horizontal line every 100 pixels
        for i in range(0, h, 100):
            self.canvas.create_line([(0, i), (w, i)])

    # Initalize the main window, canvas and their parameters
    def create_window(self):
        # Set the size of the window
        self.window.geometry(str(self.width) + "00x" + str(self.height + 2) + "60")

        # Create a canvas
        self.canvas = Canvas(self.window, width=self.width * 100, height=1000)
        self.canvas.pack()

        # Call the function to create the grid
        self.canvas.bind('<Configure>', self.create_grid)

        self.window.resizable(False, False)

    # Function called to update the displayed environment and its related values
    def update_display(self, env: Environment):
        house: House = env.house
        pos_robot = env.robot_positions[0]
        current_robot: Robot = pos_robot[0]
        action_plan = current_robot.get_action_plan()

        # Check values in the House to display dust and diamonds
        for i in range(self.width):
            for j in range(self.height):
                self.canvas.delete(self.grid[i][j])
                if house.get_room_at(i, j).has_jewel_and_dust():
                    self.grid[i][j] = self.canvas.create_image(50 + 100 * i, 50 + 100 * j, anchor=CENTER,
                                                               image=self.imgDustDiamonds)
                elif house.get_room_at(i, j).has_jewel():
                    self.grid[i][j] = self.canvas.create_image(50 + 100 * i, 50 + 100 * j, anchor=CENTER,
                                                               image=self.imgDiamonds)
                elif house.get_room_at(i, j).has_dust():
                    self.grid[i][j] = self.canvas.create_image(50 + 100 * i, 50 + 100 * j, anchor=CENTER,
                                                               image=self.imgDust)

        # Display aspirobot here
        self.canvas.delete(self.displayRobot)
        self.displayRobot = self.canvas.create_image(50 + 100 * pos_robot[1][0], 50 + 100 * pos_robot[1][1],
                                                     anchor=CENTER,
                                                     image=self.imgAspirobot)

        # ---------------------------------------INFOS DISPLAY SECTION--------------------------------------------------
        self.canvas.delete(self.line1)
        self.line1 = self.canvas.create_text(20, 510, fill="darkblue", font="Helvetica 10 bold",
                                             text="----------------------------------------------- ASPIROBOT "
                                                  "------------------------------------------------ ", anchor=NW)

        # Get number of iterations done from the robot
        iterationsValue = current_robot.get_nb_iterations()

        self.canvas.delete(self.displayExploration)
        self.canvas.delete(self.displayMetric)

        # Display type of exploration and the metric
        if iterationsValue < 5:  # Non Informed exploration (no metric)
            self.displayExploration = self.canvas.create_text(20, 530, fill="darkblue", font="Helvetica 10 bold",
                                                              text="Exploration utilisée : Informée", anchor=NW)

            self.displayMetric = self.canvas.create_text(20, 650, fill="darkblue", font="Helvetica 10 bold",
                                                         text="Métrique (distance à l'objet le plus proche) : "
                                                              "Non utilisée en non informée",
                                                         anchor=NW)
        else:  # Informed exploration metric
            self.displayExploration = self.canvas.create_text(20, 530, fill="darkblue", font="Helvetica 10 bold",
                                                              text="Exploration utilisée : Non informée", anchor=NW)

            self.displayMetric = self.canvas.create_text(20, 650, fill="darkblue", font="Helvetica 10 bold",
                                                         text="Métrique (distance à l'objet le plus proche) : " +
                                                              str(self.metricValue),
                                                         anchor=NW)

        # Display number of iterations done
        self.canvas.delete(self.displayIterations)
        self.displayIterations = self.canvas.create_text(20, 550, fill="darkblue", font="Helvetica 10 bold",
                                                         text="Nombre d'itérations effectuées : " + str(
                                                             iterationsValue), anchor=NW)

        # Display the action plan
        self.canvas.delete(self.displayPlan)
        self.displayPlan = self.convert_action_plan(action_plan, house)
        self.displayPlan = self.canvas.create_text(20, 590, fill="darkblue", font="Helvetica 10 bold",
                                                   text="Plan d'action en cours : " + self.list_to_string(
                                                       self.displayPlan), anchor=NW)

        # Display closer diamond / dust (goal)
        self.canvas.delete(self.displayGoal)
        self.displayGoal = action_plan[len(action_plan) - 1]
        # Display the action plan
        self.displayGoal = self.canvas.create_text(20, 630, fill="darkblue", font="Helvetica 10 bold",
                                                   text="Cible (diamant ou poussière la plus proche) : " + str(
                                                       self.displayGoal),
                                                   anchor=NW)

        # Display vacuumed dust value
        dustValue = current_robot.get_vacuumed_dust()
        self.canvas.delete(self.displayVacuumedDust)
        self.displayVacuumedDust = self.canvas.create_text(20, 690, fill="darkblue", font="Helvetica 10 bold",
                                                           text="Poussière aspirée : " + str(
                                                               dustValue),
                                                           anchor=NW)

        # Display collected diamonds value
        diamondsValue = current_robot.get_collected_diamonds()
        self.canvas.delete(self.displayCollectedDiamonds)
        self.displayCollectedDiamonds = self.canvas.create_text(20, 710, fill="darkblue", font="Helvetica 10 bold",
                                                                text="Diamants collectés : " + str(
                                                                    diamondsValue),
                                                                anchor=NW)

        # Display vacuumed diamonds value
        vaccumedDiamondsValue = current_robot.get_vacuumed_diamonds()
        self.canvas.delete(self.displayVacuumedDiamonds)
        self.displayVacuumedDiamonds = self.canvas.create_text(20, 730, fill="darkblue", font="Helvetica 10 bold",
                                                               text="Diamants aspirés : " + str(
                                                                   vaccumedDiamondsValue),
                                                               anchor=NW)

    # Converts the list of positions from the robot's action plan to string to display it
    def convert_action_plan(self, action_plan, house: House):
        new_action_plan = []
        for i in range(1, len(action_plan)):
            prec = action_plan[i - 1]
            if prec[0] < action_plan[i][0]:
                new_action_plan.append("Droite")
            elif prec[0] > action_plan[i][0]:
                new_action_plan.append("Gauche")
            elif prec[1] > action_plan[i][1]:
                new_action_plan.append("Haut")
            elif prec[1] < action_plan[i][1]:
                new_action_plan.append("Bas")

        # if the action plan is not empty
        if action_plan:
            goal_x = action_plan[len(action_plan) - 1][0]
            goal_y = action_plan[len(action_plan) - 1][1]
            if house.get_room_at(goal_x, goal_y).has_jewel_and_dust():
                new_action_plan.append("Aspirer")
            elif house.get_room_at(goal_x, goal_y).has_jewel():
                new_action_plan.append("Collecter")
            elif house.get_room_at(goal_x, goal_y).has_dust():
                new_action_plan.append("Aspirer")
                self.metricValue += 1

        return new_action_plan

    # Converts a list of string into a single string
    def list_to_string(self, list_string):
        str_end = ""

        for ele in list_string:
            str_end += (ele + " ")

        return str_end

    def get_window(self):
        return self.window
