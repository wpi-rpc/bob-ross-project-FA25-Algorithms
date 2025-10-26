"""
Draw Canny edge/path output using Python's turtle module.

Usage:
    python3 turtle_draw.py

Notes:
- This uses OpenCV contours for smoother, more organized edge drawing.
- For large images, the script automatically adjusts the scale to fit the window.
- The turtle draws each contour as a continuous line.
"""

import cv2 as cv
import turtle
import numpy as np
from image_processing import process_image

# Process the image
edges, path, points, contours_result = process_image('ronaldo.jpeg')
contours = contours_result[0]  # OpenCV returns contours as a list of arrays

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

# Draw using contours
turtle.pensize(1)

for contour in contours:
    # Start a new contour
    turtle.penup()
    
    # Simplify the contour to reduce drawing time while maintaining shape
    epsilon = 0.02 * cv.arcLength(contour, True)
    approx_contour = cv.approxPolyDP(contour, epsilon, True)
    
    # Draw the contour
    for i, point in enumerate(approx_contour):
        x, y = point[0]  # OpenCV contour points are in [[[x, y]]] format
        
        # Convert coordinates to turtle space (centered, y-flipped)
        turtle_x = (x - edges.shape[1]/2) * scale
        turtle_y = (edges.shape[0]/2 - y) * scale
        
        if i == 0:
            turtle.goto(turtle_x, turtle_y)
            turtle.pendown()
        else:
            turtle.goto(turtle_x, turtle_y)
    
    # Close the contour by returning to the first point
    if len(approx_contour) > 2:  # Only close if it's a proper shape
        first_point = approx_contour[0][0]
        turtle_x = (first_point[0] - edges.shape[1]/2) * scale
        turtle_y = (edges.shape[0]/2 - first_point[1]) * scale
        turtle.goto(turtle_x, turtle_y)

turtle.update()
turtle.done()
