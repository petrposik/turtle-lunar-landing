import random
import turtle
import time
import math

# Game parameters
N_STARS = 100
ROTATION_STEP = 0.2
SPEED_STEP = 0.1
GRAVITY = 0.03
# Lunar module design parameters
BRANCH_SIZE = 40
N_DISCS = 5
DISC_COLOR = "light gray"
CENTER_COLOR = "gold"
LANDING_GEAR_COLOR = "RED"
# Landing parameters
LANDING_PAD_POSITION = (0, -200)
MODULE_LANDING_POSITION = (
    LANDING_PAD_POSITION[0],
    LANDING_PAD_POSITION[1] + BRANCH_SIZE,
)
LANDING_POS_TOL_X = 20
LANDING_POS_TOL_Y = 5
LANDING_ORIENTATION = 270
LANDING_ORI_TOL = 15


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


class LandingPad(turtle.Turtle):
    def __init__(self, position):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.setposition(position)

    def draw(self):
        self.pendown()
        self.pensize(10)
        self.forward(BRANCH_SIZE / 2)
        self.forward(-BRANCH_SIZE)
        self.forward(BRANCH_SIZE / 2)
        self.penup()

    def check_landing(self, lunar_module: "LunarModule"):
        if (
            abs(lunar_module.xcor() - MODULE_LANDING_POSITION[0]) < LANDING_POS_TOL_X
            and abs(lunar_module.ycor() - MODULE_LANDING_POSITION[1])
            < LANDING_POS_TOL_Y
        ):
            if abs(lunar_module.heading() - LANDING_ORIENTATION) < LANDING_ORI_TOL:
                lunar_module.setposition(MODULE_LANDING_POSITION)
                lunar_module.setheading(LANDING_ORIENTATION)
                lunar_module.deactivate_left_thruster()
                lunar_module.deactivate_right_thruster()
                lunar_module.draw()
                return True
            else:
                # Crash on landing pad - wrong angle
                lunar_module.deactivate_left_thruster()
                lunar_module.deactivate_right_thruster()
                lunar_module.draw()
                return False
        if lunar_module.ycor() < self.screen.window_height() / -2:
            # Crash on landing pad - too low
            lunar_module.deactivate_left_thruster()
            lunar_module.deactivate_right_thruster()
            lunar_module.draw()
            return False
        return None  # No (un)successful landing yet


class LunarModule(turtle.Turtle):
    def __init__(self, position, rotation_speed=0, speed=0, direction=0):
        super().__init__()
        self.rotation_speed = rotation_speed
        self.travel_speed = speed
        self.travel_direction = direction
        self.left_thruster = False
        self.right_thruster = False
        self.fuel = turtle.Turtle()
        self.fuel.penup()
        self.fuel.hideturtle()
        self.penup()
        self.hideturtle()
        self.setposition(position)
        window = self.getscreen()
        window.onkeypress(self.activate_left_thruster, "Left")
        window.onkeypress(self.activate_right_thruster, "Right")
        window.onkeyrelease(self.deactivate_left_thruster, "Left")
        window.onkeyrelease(self.deactivate_right_thruster, "Right")
        window.listen()

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
        # Draw burning fuel
        self.fuel.clear()
        if self.left_thruster:
            self.draw_burning_fuel("left")
        if self.right_thruster:
            self.draw_burning_fuel("right")

    def draw_burning_fuel(self, thruster):
        direction = 1 if thruster == "left" else -1
        self.fuel.penup()
        self.fuel.setposition(self.position())
        self.fuel.setheading(self.heading())
        self.fuel.right(direction * 360 / N_DISCS)
        self.fuel.forward(BRANCH_SIZE)
        self.fuel.left(direction * 360 / N_DISCS)
        # Draw burning fuel
        self.fuel.pendown()
        self.fuel.pensize(8)
        self.fuel.color("yellow")
        self.fuel.forward(BRANCH_SIZE)
        self.fuel.backward(BRANCH_SIZE)
        self.fuel.left(7)
        self.fuel.color("red")
        self.fuel.pensize(4)
        for _ in range(2):
            self.fuel.forward(BRANCH_SIZE)
            self.fuel.backward(BRANCH_SIZE)
            self.fuel.right(14)

    def activate_left_thruster(self):
        self.left_thruster = True

    def activate_right_thruster(self):
        self.right_thruster = True

    def deactivate_left_thruster(self):
        self.left_thruster = False

    def deactivate_right_thruster(self):
        self.right_thruster = False

    def update(self):
        # Rotation
        if self.left_thruster:
            self.rotation_speed -= ROTATION_STEP
        if self.right_thruster:
            self.rotation_speed += ROTATION_STEP
        self.left(self.rotation_speed)
        # Translation
        dx = self.travel_speed * math.cos(math.radians(self.travel_direction))
        dy = self.travel_speed * math.sin(math.radians(self.travel_direction))
        self.setx(self.xcor() + dx)
        self.sety(self.ycor() + dy)
        # Acceleration
        if self.left_thruster and self.right_thruster:
            self.apply_force("thrusters")
        self.apply_force("gravity")

    def apply_force(self, mode):
        tangential = self.travel_speed
        normal = 0
        if mode == "gravity":
            force_direction = -90
            step = GRAVITY
        elif mode == "thrusters":
            force_direction = self.heading() + 180
            step = SPEED_STEP
        angle = force_direction - self.travel_direction
        tangential += step * math.cos(math.radians(angle))
        normal += step * math.sin(math.radians(angle))
        direction_change = math.degrees(math.atan2(normal, tangential))
        self.travel_direction += direction_change
        self.travel_speed = math.hypot(tangential, normal)


if __name__ == "__main__":
    window = init_turtle_window()
    height = window.window_height()
    width = window.window_width()
    create_stars()
    create_moon()
    landing_pad = LandingPad(LANDING_PAD_POSITION)
    landing_pad.draw()
    lunar_module = LunarModule(
        position=(-width / 3, height / 3),
        rotation_speed=random.randint(-5, 5),
        speed=random.randint(1, 3),
        direction=random.randint(-45, 0),
    )

    while True:
        lunar_module.update()
        lunar_module.draw()
        successful_landing = landing_pad.check_landing(lunar_module)
        if successful_landing is not None:
            if successful_landing:
                window.title("Successful landing! Well done!")
            else:
                window.bgcolor("red")
                window.title("Crash!")
            break
        window.update()
        time.sleep(0.05)

    turtle.done()
