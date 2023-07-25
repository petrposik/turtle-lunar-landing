import random
import turtle

# Game parameters
N_STARS = 100
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
    def __init__(self, position):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.setposition(*position)

    def draw(self):
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


if __name__ == "__main__":
    window = init_turtle_window()
    height = window.window_height()
    width = window.window_width()
    create_stars()
    create_moon()
    lunar_module = LunarModule((-width / 3, height / 3))
    lunar_module.draw()
    window.update()
    turtle.done()
