import cv2
import os
import time
from imageProcessing import (
    grayscale,
    gaussian_blur,
    sobel_edge,
    sharpen,
    adjust_brightness
)

# Process a single image using a fixed image processing pipeline
def process_image(input_path, output_path=None, save=False):

    # Read image from file
    img = cv2.imread(input_path)
    if img is None:
        return

    # Apply image processing operations
    img = grayscale(img)
    img = gaussian_blur(img)
    img = sobel_edge(img)
    img = sharpen(img)
    img = adjust_brightness(img, value=20)

    # Save processed image if required
    if save and output_path:
        cv2.imwrite(output_path, img)

# Run serial processing on all images 
def run_serial(input_folder, output_folder=None, save=False):
    if save and output_folder:
        os.makedirs(output_folder, exist_ok=True)

    # Process images one by one
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            input_path = os.path.join(input_folder, filename)
            output_path = (
                os.path.join(output_folder, filename)
                if save and output_folder
                else None
            )
            process_image(input_path, output_path, save)

# Measure execution time of the serial implementation
def measure_serial(input_folder):
    start = time.time()
    run_serial(input_folder, save=False)
    return time.time() - start
