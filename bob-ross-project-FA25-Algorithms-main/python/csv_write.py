import cv2 as cv
import turtle
import csv
from edge_path_planning import edge_path_coordinates
from color_path_planning import color_path_coordinates
IMAGE = 'jordan.png'
IMAGE_SIZE = (240, 180)
# Process the image
gray_img = cv.imread(IMAGE, cv.IMREAD_GRAYSCALE) # choose the image you want here
gray_img = cv.resize(gray_img, IMAGE_SIZE)
assert gray_img is not None, "file could not be read, check with os.path.exists()"
edges = cv.Canny(gray_img,100,250) # edge detection function (parameters can be adjusted)
color_img = cv.imread(IMAGE)
color_img = cv.resize(color_img, IMAGE_SIZE)

edge_path = edge_path_coordinates(edges)

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

with open('edge_path.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Draw streaks greedily by always going to the nearest remaining streak
    # Start current position at image center (corresponds to turtle origin)
    current_pixel = (edge_path[0][0][0], edge_path[0][0][1])
    # Try to find a nearby streak by scanning outward from the current endpoint.
    # If no streak is found within the expanding radii, fall back to global nearest.
    while len(edge_path) > 0:
        idx = None
        # radii (in pixels) to try — small -> larger. Tune these for your images.
        for radius in (4, 8, 16, 32, 64, 128):
            idx = _find_nearest_streak_within_radius(edge_path, current_pixel, radius)
            if idx is not None:
                break
        if idx is None:
            idx = _find_nearest_streak_index(edge_path, current_pixel)
        if idx is None:
            break
        streak = edge_path.pop(idx)
        if len(streak) == 0:
            continue
        writer.writerow(streak)
        # set current pixel to the last point in the streak so next search is relative to
        # where the turtle just finished drawing
        current_pixel = streak[-1]

with open('color_path.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    color_path = color_path_coordinates(edges, color_img)
    for streak in color_path:
        # If the streak is empty or white, just skip it
        if (len(streak) == 0) or streak[2] == "white":
            continue
        writer.writerow(streak)
    