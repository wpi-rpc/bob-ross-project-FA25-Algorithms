import cv2 as cv
import turtle
import math
from path_planning import path_coordinates

# Process the image
img = cv.imread('ryan.jpg', cv.IMREAD_GRAYSCALE) # choose the image you want here
assert img is not None, "file could not be read, check with os.path.exists()"
edges = cv.Canny(img,100,250) # edge detection function (parameters can be adjusted)

path = path_coordinates(edges)

# Set up the turtle window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
turtle.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
turtle.speed(0)
turtle.hideturtle()
turtle.tracer(False)  # disable animation for faster drawing

# Calculate scale to fit image in window while preserving aspect ratio
# width_scale = (WINDOW_WIDTH * 0.8) / path.shape[1]
# height_scale = (WINDOW_HEIGHT * 0.8) / path.shape[0]
# scale = min(width_scale, height_scale)

# Draw using the ordered path
turtle.pensize(2)
first_point = True

# Loops for every streak (drawing segment) in the path
for streak in path:
    for (x, y) in streak:  # Use every 3rd point for speed while maintaining path order
        if first_point: # lifts pen point for the first point in every streak
            turtle.penup()
            first_point = False
        else: # puts it down for every other point
            turtle.pendown()
        # Convert image pixel coordinates to turtle coordinates )
        turtle_x = (x - edges.shape[1]/2) * 1
        turtle_y = (edges.shape[0]/2 - y) * 1
        turtle.goto(turtle_x, turtle_y) # move turtle to the calculated position
        turtle.update()
    turtle.penup()  # lift pen between streaks
    first_point = True

turtle.done()



