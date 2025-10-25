import cv2
import numpy as np

def apply_sobel(gray, direction="Both", ksize=3):
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)

    if direction == "X":
        edges = sobelx
    elif direction == "Y":
        edges = sobely
    else:  
        edges = cv2.magnitude(sobelx, sobely)

    return np.uint8(np.absolute(edges))
