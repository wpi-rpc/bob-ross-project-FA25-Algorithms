import cv2 as cv
import turtle
from edge_path_planning import edge_path_coordinates
from color_path_planning import color_path_coordinates
IMAGE = 'jordan.png'
#240, 180
IMAGE_SIZE = (1000, 1000)
# Process the image
gray_img = cv.imread(IMAGE, cv.IMREAD_GRAYSCALE) # choose the image you want here
gray_img = cv.resize(gray_img, IMAGE_SIZE)
assert gray_img is not None, "file could not be read, check with os.path.exists()"
edges = cv.Canny(gray_img,100,250) # edge detection function (parameters can be adjusted)
color_img = cv.imread(IMAGE)
color_img = cv.resize(color_img, IMAGE_SIZE)

edge_path = edge_path_coordinates(edges)

# Set up the turtle window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
turtle.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
turtle.speed(10)
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
for streak in edge_path:
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


color_path = color_path_coordinates(edges, color_img)
for streak in color_path:
    # If the streak is empty or white, just skip it
    if (len(streak) == 0) or streak[2] == "white":
        continue
    start = streak[0]
    end = streak[1]
    turtle.color(streak[2])
    turtle.penup()
    turtle.goto((start[1] - edges.shape[1]/2) + 1, (edges.shape[0]/2 - start[0]))
    turtle.pendown()
    turtle.goto((end[1] - edges.shape[1]/2), (edges.shape[0]/2 - end[0]))
    turtle.update()

turtle.done()


