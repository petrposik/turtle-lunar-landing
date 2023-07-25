import random
import turtle

# Game parameters
N_STARS = 100


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


if __name__ == "__main__":
    window = init_turtle_window()
    create_stars()
    create_moon()
    window.update()
    turtle.done()

