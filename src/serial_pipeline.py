import cv2
import os
import time
from filters import grayscale, gaussian_blur, sobel_edge, sharpen, adjust_brightness

def process_image(input_path, output_path):
    """Run all filters sequentially on one image."""
    img = cv2.imread(input_path)

    if img is None:
        print(f"Failed to load {input_path}")
        return

    img = grayscale(img)
    img = gaussian_blur(img)
    img = sobel_edge(img)
    img = sharpen(img)
    img = adjust_brightness(img, value=20)

    cv2.imwrite(output_path, img)

def run_serial(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            inp = os.path.join(input_folder, filename)
            out = os.path.join(output_folder, filename)
            process_image(inp, out)

def measure_serial(input_folder, output_folder):
    start = time.time()
    run_serial(input_folder, output_folder)
    end = time.time()
    return end - start

if __name__ == "__main__":
    inp = "../data/subset_1000"
    out = "../results/serial"
    t = measure_serial(inp, out)
    print(f"Serial execution time: {t:.4f} seconds")
