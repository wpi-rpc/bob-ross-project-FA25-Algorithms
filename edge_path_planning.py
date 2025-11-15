def edge_path_coordinates(image):
    path = []
    streak = generate_edge_streak(image, (0,0))
    # Keep going as long as drawing streak is present
    while len(streak) > 0:
        # Ignore streaks that are too short, not significant enough
        if len(streak) > 2:
            path.append(streak)
        streak = generate_edge_streak(image, streak[-1])
    return path

def generate_edge_streak(image, starting_point):
    streak = []
    queue = []
    # Find first white pixel in the image
    if starting_point == (0, 0):
        i = 0
        for row in image:
            if 255 in row:
                queue.append((row.tolist().index(255), i))
                break
            i+=1
    else:
        closest = find_closest_white(starting_point, image)
        if closest:
            queue.append(closest)

    while len(queue) > 0:
        current = queue.pop(0)
        if image[current[1]][current[0]] == 255:
            # Mark pixel as visited by coloring it gray
            image[current[1]][current[0]] = 128
            streak.append(current)
            neighbors = get_neighbors(current, image)
            # Sort neighbors by number of white pixels surrounding them (smaller number of white pixels means it's more likely to be an edge)
            if len(neighbors) > 1:
                # Reverse because we want pixels with fewer white neighbors to be explored first
                neighbors.sort(key=lambda x: len(get_neighbors(x, image)))
            
            if len(neighbors) > 0 and neighbors[0] not in queue:
                queue.insert(0, neighbors[0])
                    
    return streak

# Returns all white pixel neighbors of a given pixel
def get_neighbors(pixel, image):
    neighbors = []
    x, y = pixel
    # Neigbors below pixel
    if y > 0:
        if image[y-1][x] == 255:
            neighbors.append((x, y-1))
        if x > 0 and image[y-1][x-1] == 255:
            neighbors.append((x-1, y-1))
        if x < len(image[0])-1 and image[y-1][x+1] == 255:
            neighbors.append((x+1, y-1))
    # Neighbors above pixel
    if y < len(image)-1:
        if image[y+1][x] == 255:
            neighbors.append((x, y+1))
        if x > 0 and image[y+1][x-1] == 255:
            neighbors.append((x-1, y+1))
        if x < len(image[0])-1 and image[y+1][x+1] == 255:
            neighbors.append((x+1, y+1))
    # Neighbors left and right of pixel
    if x > 0 and image[y][x-1] == 255:
        neighbors.append((x-1, y))
    if x < len(image[0])-1 and image[y][x+1] == 255:
        neighbors.append((x+1, y))
    
    return neighbors

# Searches for closest white pixel in a spiral
def find_closest_white(pixel, image):
    x, y = pixel
    limit_x = len(image[0])
    limit_y = len(image)
    # By how much the coordinate changes each round
    change = 1
    # How much we want it to change by before switching direction
    change_target = 1
    # IF the direction is x
    changing_x = True
    # By how much coordinate has changed in this iteration
    changed_by = 0
    # If done full row check, then there must be no white anymore
    while abs(change_target) <= max(limit_x, limit_y):
        if (image[y][x] == 255):
            return (x, y)
        else:
            if changing_x:
                x += change
                changed_by += change
                # CHeck if at edges or if we have moved desired amount for iteration. If so, switch to y direction
                if x == limit_x:
                    x = limit_x - 1
                    changed_by = 0
                    changing_x = False
                elif x == -1:
                    x = 0
                    changed_by = 0
                    changing_x = False
                elif changed_by == change_target:
                    changed_by = 0
                    changing_x = False
            else:
                y += change
                changed_by += change
                # Check if at edges or moved desired amount for iteration. If so, switch to x direction, ensure we go opposite direction as before,
                # and add 1 to how much we want to move for current iteration
                if y == limit_y:
                    y = limit_y - 1
                    changed_by = 0
                    change *= -1
                    change_target *= -1
                    change_target += change
                    changing_x = True
                elif y == -1:
                    y = 0
                    changed_by = 0
                    change *= -1
                    change_target *= -1
                    change_target += change
                    changing_x = True
                elif changed_by == change_target:
                    changed_by = 0
                    change *= -1
                    change_target *= -1
                    change_target += change
                    changing_x = True