import os
import cv2
import time
from concurrent.futures import ThreadPoolExecutor
from imageProcessing import (
    grayscale,
    gaussian_blur,
    sobel_edge,
    sharpen,
    adjust_brightness
)

# Process one image
def process_image_cf(input_path):
    # Read image
    img = cv2.imread(input_path)
    if img is None:
        return

    # Apply image processing operations
    img = grayscale(img)
    img = gaussian_blur(img)
    img = sobel_edge(img)
    img = sharpen(img)
    img = adjust_brightness(img, 20)


# Run multithreading using ThreadPoolExecutor
def run_cf(input_folder, workers=1):
    # Create task list
    tasks = [
        os.path.join(input_folder, f)
        for f in os.listdir(input_folder)
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

    # Execute tasks in parallel
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(process_image_cf, tasks)


# Measure execution time
def measure_cf(input_folder, workers):
    start = time.time()
    run_cf(input_folder, workers=workers)
    return time.time() - start
