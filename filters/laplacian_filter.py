import cv2
import numpy as np

def apply_laplacian(gray, ksize=3):
   
    edges = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
    return np.uint8(np.absolute(edges))
