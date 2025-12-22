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

def process_image(input_path, output_path=None, save=False):
    img = cv2.imread(input_path)
    if img is None:
        return

    img = grayscale(img)
    img = gaussian_blur(img)
    img = sobel_edge(img)
    img = sharpen(img)
    img = adjust_brightness(img, value=20)

    if save and output_path:
        cv2.imwrite(output_path, img)

def run_serial(input_folder, output_folder=None, save=False):
    if save and output_folder:
        os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            input_path = os.path.join(input_folder, filename)
            output_path = (
                os.path.join(output_folder, filename)
                if save and output_folder
                else None
            )
            process_image(input_path, output_path, save)

def measure_serial(input_folder):
    start = time.time()
    run_serial(input_folder, save=False)
    return time.time() - start
