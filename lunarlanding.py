import random
import turtle

# Set up the game window
window = turtle.Screen()
window.tracer(0)
window.setup(0.6, 0.6)
window.title("Lunar Landing Game")
window.bgcolor("black")

width = window.window_width()
height = window.window_height()

# Game parameters
n_stars = 100

# Stars and Moon
stars = turtle.Turtle()
stars.hideturtle()
stars.penup()
stars.color("white")
for _ in range(n_stars):
    # Use floor division to ensure ints in randint()
    x_pos = random.randint(-width // 2, width // 2)
    y_pos = random.randint(-height // 2, height // 2)
    stars.setposition(x_pos, y_pos)
    stars.dot(random.randint(2, 6))

moon = turtle.Turtle()
moon.penup()
moon.color("slate gray")
moon.sety(-height * 2.8)
moon.dot(height * 5)

window.update()
turtle.done()

