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

# --------------------------------------------------
# Image Processing Task
# --------------------------------------------------
def process_image_cf(args):
    input_path, output_path, save = args

    img = cv2.imread(input_path)
    if img is None:
        return

    img = grayscale(img)
    img = gaussian_blur(img)
    img = sobel_edge(img)
    img = sharpen(img)
    img = adjust_brightness(img, 20)

    if save and output_path:
        cv2.imwrite(output_path, img)


# --------------------------------------------------
# Run Concurrent.Futures (Multithreading)
# --------------------------------------------------
def run_cf(input_folder, output_folder=None, workers=1, save=False):
    if save and output_folder:
        os.makedirs(output_folder, exist_ok=True)

    tasks = [
        (
            os.path.join(input_folder, f),
            os.path.join(output_folder, f) if save else None,
            save
        )
        for f in os.listdir(input_folder)
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(process_image_cf, tasks)

# --------------------------------------------------
# Measure execution time
# --------------------------------------------------
def measure_cf(input_folder, workers):
    start = time.time()
    run_cf(input_folder, workers=workers, save=False)
    return time.time() - start

