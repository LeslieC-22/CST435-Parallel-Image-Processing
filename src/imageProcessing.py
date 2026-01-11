import cv2
import numpy as np

# Convert BGR image to grayscale
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply 3×3 Gaussian blur
def gaussian_blur(img):
    return cv2.GaussianBlur(img, (3, 3), sigmaX=0)

def sobel_edge(img):
    # Apply Sobel operator in the x-direction to detect vertical edges
    gx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)

    # Apply Sobel operator in the y-direction to detect horizontal edges
    gy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    # Compute gradient magnitude using Euclidean distance
    magnitude = np.sqrt(gx**2 + gy**2)

    # Normalize the magnitude values to the range [0, 255]
    max_val = magnitude.max()
    if max_val > 0:
        magnitude = (magnitude / max_val) * 255
    else:
        magnitude = np.zeros_like(magnitude)

    # Convert result to 8-bit unsigned integer format
    return magnitude.astype(np.uint8)

# Sharpen image using a fixed kernel
def sharpen(img):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(img, -1, kernel)

# Increase or decrease brightness
def adjust_brightness(img, value=20):
    bright = img.astype(np.int16) + value
    bright = np.clip(bright, 0, 255)
    return bright.astype(np.uint8)
