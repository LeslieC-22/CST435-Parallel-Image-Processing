import os
import cv2
import time
from multiprocessing import Pool, cpu_count
from imageProcessing import grayscale, gaussian_blur, sobel_edge, sharpen, adjust_brightness

def process_image_mp(args):
    input_path, output_path = args
    img = cv2.imread(input_path)
    if img is None:
        return

    img = grayscale(img)
    img = gaussian_blur(img)
    img = sobel_edge(img)
    img = sharpen(img)
    img = adjust_brightness(img, 20)

    cv2.imwrite(output_path, img)

def run_mp(input_folder, output_folder, workers):
    os.makedirs(output_folder, exist_ok=True)
    files = [
        (os.path.join(input_folder, f), os.path.join(output_folder, f))
        for f in os.listdir(input_folder)
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]
    with Pool(processes=workers) as pool:
        pool.map(process_image_mp, files)

def measure_mp(input_folder, output_folder, workers):
    start = time.time()
    run_mp(input_folder, output_folder, workers)
    return time.time() - start

if __name__ == "__main__":

    datasets = {
        "100 images": "../dataset/images_100",
        "5000 images": "../dataset/images_5000"
    }

    out_base = "../results/multiprocessing"

    max_cpu = cpu_count()
    worker_counts = [1, 2, 4, 8, 16]
    worker_counts = [w for w in worker_counts if w <= max_cpu]

    print("\nPerformance Results")
    for dataset_name, dataset_path in datasets.items():
        print(f"\n==============================")
        print(f"Dataset: {dataset_name}")
        print(f"==============================")

        results = []

        # Serial 
        serial_time = measure_mp(
            dataset_path,
            f"{out_base}_{dataset_name.replace(' ', '_')}_1",
            1
        )

        results.append((1, serial_time, 1.0, 1.0))

        # Parallel 
        for w in worker_counts[1:]:
            parallel_time = measure_mp(
                dataset_path,
                f"{out_base}_{dataset_name.replace(' ', '_')}_{w}",
                w
            )
            speedup = serial_time / parallel_time
            efficiency = speedup / w
            results.append((w, parallel_time, speedup, efficiency))

        # Print results table
        print(f"{'Workers':>8} | {'Time (s)':>10} | {'Speedup':>8} | {'Efficiency':>10}")
        print("-" * 46)

        for w, t, s, e in results:
            print(f"{w:>8} | {t:>10.4f} | {s:>8.2f} | {e:>10.2f}")
