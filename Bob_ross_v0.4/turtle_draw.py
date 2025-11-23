import cv2 as cv
import turtle
import math
from path_planning import path_coordinates

# Process the image
img = cv.imread('ryan.jpg', cv.IMREAD_GRAYSCALE) # choose the image you want here
assert img is not None, "file could not be read, check with os.path.exists()"
edges = cv.Canny(img,100,250) # edge detection function (parameters can be adjusted)

path = path_coordinates(edges)

# Helper: find index of the streak whose nearest point is closest to `current`
def _find_nearest_streak_index(path_list, current):
    best_idx = None
    best_dist = float('inf')
    cx, cy = current
    for i, streak in enumerate(path_list):
        for (x, y) in streak:
            d = (x - cx) ** 2 + (y - cy) ** 2
            if d < best_dist:
                best_dist = d
                best_idx = i
    return best_idx


# Find nearest streak whose any point lies within `radius` of `current`.
# Returns the index of the best matching streak or None if none found.
def _find_nearest_streak_within_radius(path_list, current, radius):
    best_idx = None
    best_dist = float('inf')
    cx, cy = current
    r2 = radius * radius
    for i, streak in enumerate(path_list):
        for (x, y) in streak:
            dx = x - cx
            dy = y - cy
            d2 = dx*dx + dy*dy
            if d2 <= r2 and d2 < best_dist:
                best_dist = d2
                best_idx = i
    return best_idx

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

# Draw streaks greedily by always going to the nearest remaining streak
# Start current position at image center (corresponds to turtle origin)
current_pixel = (edges.shape[1] // 2, edges.shape[0] // 2)
# Try to find a nearby streak by scanning outward from the current endpoint.
# If no streak is found within the expanding radii, fall back to global nearest.
while len(path) > 0:
    idx = None
    # radii (in pixels) to try — small -> larger. Tune these for your images.
    for radius in (4, 8, 16, 32, 64, 128):
        idx = _find_nearest_streak_within_radius(path, current_pixel, radius)
        if idx is not None:
            break
    if idx is None:
        idx = _find_nearest_streak_index(path, current_pixel)
    if idx is None:
        break
    streak = path.pop(idx)
    if len(streak) == 0:
        continue
    for (x, y) in streak:
        if first_point:
            turtle.penup()
            first_point = False
        else:
            turtle.pendown()
        # Convert image pixel coordinates to turtle coordinates
        turtle_x = (x - edges.shape[1]/2) * 1
        turtle_y = (edges.shape[0]/2 - y) * 1
        turtle.goto(turtle_x, turtle_y)
        turtle.update()
    turtle.penup()
    first_point = True
    # set current pixel to the last point in the streak so next search is relative to
    # where the turtle just finished drawing
    current_pixel = streak[-1]

turtle.done()



