"""
Draw Canny edge/path output using Python's turtle module.

Usage:
    python3 turtle_draw.py

Notes:
- This uses path_planning.path_coordinates to obtain an ordered path of edge pixels.
- For large images, the script automatically adjusts the scale to fit the window.
- The turtle follows the path in order, creating a more continuous drawing.
"""

import cv2 as cv
import turtle
import math
from image_processing import process_image

# Process the image
edges, path, points, contours = process_image('ronaldo.jpeg')

# Set up the turtle window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
turtle.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
turtle.speed(0)
turtle.hideturtle()
turtle.tracer(False)  # disable animation for faster drawing

# Calculate scale to fit image in window while preserving aspect ratio
width_scale = (WINDOW_WIDTH * 0.8) / edges.shape[1]
height_scale = (WINDOW_HEIGHT * 0.8) / edges.shape[0]
scale = min(width_scale, height_scale)

# Draw using the ordered path
turtle.pensize(2)
first_point = True

for (x, y) in path[::3]:  # Use every 3rd point for speed while maintaining path order
    if first_point:
        turtle.penup()
        first_point = False
    else:
        turtle.pendown()
    # Convert coordinates to turtle space (centered, y-flipped)
    turtle_x = (x - edges.shape[1]/2) * scale
    turtle_y = (edges.shape[0]/2 - y) * scale
    turtle.goto(turtle_x, turtle_y)

turtle.update()
turtle.done()
