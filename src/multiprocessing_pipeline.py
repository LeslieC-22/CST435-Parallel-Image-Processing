import os
import cv2
import time
from multiprocessing import Pool
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
def process_image_mp(args):
    """Apply required image processing filters in a separate process."""
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
# Run multiprocessing
# --------------------------------------------------
def run_mp(input_folder, output_folder=None, workers=1, save=False):
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

    with Pool(processes=workers) as pool:
        pool.map(process_image_mp, tasks)


# --------------------------------------------------
# Measurement Function (called by main.py)
# --------------------------------------------------
def measure_mp(input_folder, workers):
    start = time.time()
    run_mp(input_folder, workers=workers, save=False)
    return time.time() - start


