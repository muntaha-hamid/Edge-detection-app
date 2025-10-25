import cv2

def apply_canny(gray, threshold1=50, threshold2=150, ksize=3, sigma=1.0):

    blurred = cv2.GaussianBlur(gray, (ksize, ksize), sigma)
    edges = cv2.Canny(blurred, threshold1, threshold2)
    return edges
