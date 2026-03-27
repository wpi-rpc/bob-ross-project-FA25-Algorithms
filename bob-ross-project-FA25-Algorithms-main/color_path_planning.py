colors = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "cyan": (255, 255, 0),
    "magenta": (255, 0, 255),
    "yellow": (0, 255, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}

# Gets average color between two rows, horizontal says whether going left right or up down, step says whether going forwards or backwards
def get_average_color(bgr_image, start, end, horizontal, step=1):
    count = 0
    total_blue = 0
    total_green = 0
    total_red = 0
    # Tally up the colors from start to end
    if horizontal:
        for i in range(start[1], end[1], step):
            # NEED INT CONVERSION
            total_blue = total_blue + int(bgr_image[start[0]][i][0])
            total_green = total_green + int(bgr_image[start[0]][i][1])
            total_red = total_red + int(bgr_image[start[0]][i][2])
            count += 1
    else:
        for i in range(start[0], end[0], step):
            # NEED INT CONVERSION
            total_blue = total_blue + int(bgr_image[i][start[1]][0])
            total_green = total_green + int(bgr_image[i][start[1]][1])
            total_red = total_red + int(bgr_image[i][start[1]][2])
            count += 1
    # Average out the colors
    total_blue /= count
    total_green /= count
    total_red /= count
    
    # Look for closest color to the one we have
    closest_color = ""
    smallest_diff = 1024
    for (color, value) in colors.items():
        # Get total difference between colors
        total_diff = abs(value[0] - total_blue) + abs(value[1] - total_green) + abs(value[2] - total_red)
        if total_diff <= smallest_diff:
            smallest_diff = total_diff
            closest_color = color
    return closest_color

def color_path_coordinates(gray_image, bgr_image):
    # Path to return in first slot, color to use in second
    path = []
    # Reverse and value range is to decide if we go from left to right or right to left
    reverse = False
    value_range = []
    color = None
    for y in range(len(gray_image)):
        prev_edge = None
        # If going reverse, change the range to go backwards
        if not reverse:
            value_range = range(len(gray_image[0]))
        else:
            value_range = range(len(gray_image[0]) - 1, -1, -1)
        for x in value_range:
            current_pixel = gray_image[y][x]

            if current_pixel == 128:
                if prev_edge is not None:
                    # If reversing, have step be -1 so it goes backwards
                    if not reverse:
                        color = get_average_color(bgr_image, prev_edge, (y, x), horizontal=True)
                    else:
                        color = get_average_color(bgr_image, prev_edge, (y, x), horizontal=True, step=-1)
                    path.append([prev_edge, (y, x), color])
                prev_edge = (y, x)
        reverse = not reverse

    # Vertical Pass
    reverse = False            
    for x in range(len(gray_image[0])):
        prev_edge = None
        if not reverse:
            value_range = range(len(gray_image))
        else:
            value_range = range(len(gray_image) - 1, -1, -1)
        for y in value_range:
            current_pixel = gray_image[y][x]
            if current_pixel == 128:
                if prev_edge is not None:
                    # Put horizontal=False so the average color goes up down instead of left right
                    if not reverse:
                        color = get_average_color(bgr_image, prev_edge, (y, x), horizontal=False)
                    else:
                        color = get_average_color(bgr_image, prev_edge, (y, x), horizontal=False, step=-1)
                    path.append([prev_edge, (y, x), color])
                prev_edge = (y, x)
        reverse = not reverse
    return merge_consecutive_colors(path)

def merge_consecutive_colors(path):
    new_path = []
    for i in range(1, len(path)):
        if (path[i-1][1] == path[i][0] and path[i-1][2] == path[i][2]):
            new_path.append([path[i-1][0], path[i][1], path[i][2]])
        else:
            new_path.append(path[i])
    return new_path