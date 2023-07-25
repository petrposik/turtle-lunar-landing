import random
import turtle
import time

# Game parameters
N_STARS = 100
ROTATION_STEP = 0.2
# Lunar module design parameters
BRANCH_SIZE = 40
N_DISCS = 5
DISC_COLOR = "light gray"
CENTER_COLOR = "gold"
LANDING_GEAR_COLOR = "RED"


def init_turtle_window():
    window = turtle.Screen()
    window.tracer(0)
    window.setup(0.6, 0.6)
    window.title("Lunar Landing Game")
    window.bgcolor("black")
    return window


# Stars and Moon
def create_stars():
    """Create stars in the background"""
    stars = turtle.Turtle()
    height = stars.screen.window_height()
    width = stars.screen.window_width()
    stars.hideturtle()
    stars.penup()
    stars.color("white")
    for _ in range(N_STARS):
        # Use floor division to ensure ints in randint()
        x_pos = random.randint(-width // 2, width // 2)
        y_pos = random.randint(-height // 2, height // 2)
        stars.setposition(x_pos, y_pos)
        stars.dot(random.randint(2, 6))


def create_moon():
    """Create the moon in the background"""
    moon = turtle.Turtle()
    height = moon.screen.window_height()
    moon.penup()
    moon.color("slate gray")
    moon.sety(-height * 2.8)
    moon.dot(height * 5)


class LunarModule(turtle.Turtle):
    def __init__(self, position, rotation_speed=0):
        super().__init__()
        self.rotation_speed = rotation_speed
        self.left_thruster = False
        self.right_thruster = False
        self.penup()
        self.hideturtle()
        self.setposition(position)

    def draw(self):
        self.clear()
        position = self.position()
        heading = self.heading()
        self.pendown()
        # Landing gear
        self.pensize(5)
        self.color(LANDING_GEAR_COLOR)
        self.forward(BRANCH_SIZE)
        self.left(90)
        self.forward(BRANCH_SIZE / 2)
        self.forward(-BRANCH_SIZE)
        self.forward(BRANCH_SIZE / 2)
        self.right(90)
        self.forward(-BRANCH_SIZE)
        # Pods around the edge of the module
        self.pensize(1)
        self.color(DISC_COLOR)
        for _ in range(N_DISCS - 1):
            self.right(360 / N_DISCS)
            self.forward(BRANCH_SIZE)
            self.dot(BRANCH_SIZE / 2)
            self.forward(-BRANCH_SIZE)
        # Center of the module
        self.color(CENTER_COLOR)
        self.dot(BRANCH_SIZE)
        self.penup()
        self.setposition(position)
        self.setheading(heading)

    def activate_left_thruster(self):
        self.left_thruster = True

    def activate_right_thruster(self):
        self.right_thruster = True

    def deactivate_left_thruster(self):
        self.left_thruster = False

    def deactivate_right_thruster(self):
        self.right_thruster = False

    def update(self):
        if self.left_thruster:
            self.rotation_speed -= ROTATION_STEP
        if self.right_thruster:
            self.rotation_speed += ROTATION_STEP
        self.left(self.rotation_speed)


if __name__ == "__main__":
    window = init_turtle_window()
    height = window.window_height()
    width = window.window_width()
    create_stars()
    create_moon()
    lunar_module = LunarModule((-width / 3, height / 3))

    window.onkeypress(lunar_module.activate_left_thruster, "Left")
    window.onkeypress(lunar_module.activate_right_thruster, "Right")
    window.onkeyrelease(lunar_module.deactivate_left_thruster, "Left")
    window.onkeyrelease(lunar_module.deactivate_right_thruster, "Right")
    window.listen()

    while True:
        lunar_module.update()
        lunar_module.draw()
        window.update()
        time.sleep(0.05)

    turtle.done()
