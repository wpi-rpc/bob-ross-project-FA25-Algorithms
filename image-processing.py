import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from edge_path_planning import edge_path_coordinates

img = cv.imread('pikachu.webp', cv.IMREAD_GRAYSCALE)
bgr_img = cv.imread('pikachu.webp')
assert img is not None, "file could not be read, check with os.path.exists()"
edges = cv.Canny(img,150,400)
rgb_image = bgr_img[:, :, ::-1]
path = edge_path_coordinates(edges)

plt.subplot(121),plt.imshow(rgb_image)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
 
plt.show()

