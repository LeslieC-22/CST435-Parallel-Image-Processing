import cv2
import numpy as np

def grayscale(img):
    """Convert BGR image to grayscale."""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gaussian_blur(img):
    """Apply 3×3 Gaussian blur."""
    return cv2.GaussianBlur(img, (3, 3), sigmaX=0)

def sobel_edge(img):
    gx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    magnitude = np.sqrt(gx**2 + gy**2)
    max_val = magnitude.max()

    if max_val > 0:
        magnitude = (magnitude / max_val) * 255
    else:
        magnitude = np.zeros_like(magnitude)

    return magnitude.astype(np.uint8)

def sharpen(img):
    """Sharpen image using a fixed kernel."""
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(img, -1, kernel)

def adjust_brightness(img, value=20):
    """Increase or decrease brightness."""
    bright = img.astype(np.int16) + value
    bright = np.clip(bright, 0, 255)
    return bright.astype(np.uint8)
