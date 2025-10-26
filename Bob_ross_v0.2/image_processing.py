import numpy as np
import cv2 as cv
from path_planning import path_coordinates

def process_image(image_path):
    img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    edges = cv.Canny(img,150,400)
    path = path_coordinates(edges)
    points = np.column_stack(np.where(edges > 0))
    contours = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    return edges, path, points, contours

if __name__ == "__main__":
    # Only run this code if the script is run directly
    from matplotlib import pyplot as plt
    
    img = cv.imread('ronaldo.jpeg', cv.IMREAD_GRAYSCALE)
    edges = cv.Canny(img,150,400)
    
    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()

