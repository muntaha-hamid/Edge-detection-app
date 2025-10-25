import numpy as np
from PIL import Image
import cv2
import os

def read_image(file_input):
    """Reads an image file (uploaded file or path) and returns RGB + Grayscale versions."""
    if isinstance(file_input, str) and os.path.exists(file_input):
        image = np.array(Image.open(file_input).convert("RGB"))
    else:
        image = np.array(Image.open(file_input).convert("RGB"))

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return image, gray
