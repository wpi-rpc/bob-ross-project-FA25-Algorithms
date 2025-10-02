import numpy as np

def path_coordinates(image):
    path = []
    queue = []
    start = None
    # Find first white pixel in the image
    i = 0
    for row in image:
        if 255 in row:
            print(row.tolist().index(255))
            queue.append((row.tolist().index(255), i))
            break
        i+=1

    while len(queue) > 0:
        current = queue.pop(0)
        if image[current[1]][current[0]] == 255:
            # Mark pixel as visited by coloring it gray
            image[current[1]][current[0]] = 128
            path.append(current)
            neighbors = get_neighbors(current, image)
            # Sort neighbors by number of white pixels surrounding them (smaller number of white pixels means it's more likely to be an edge)
            if len(neighbors) > 1:
                # Reverse because we want pixels with fewer white neighbors to be explored first
                neighbors.sort(key=lambda x: len(get_neighbors(x, image)), reverse=True)
            for neighbor in neighbors:
                if neighbor not in queue:
                    queue.insert(0, neighbor)
    
    return path

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