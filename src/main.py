import os
from multiprocessing import cpu_count

# Import paradigms
import serial_pipeline as seq
import multiprocessing_pipeline as mp
import multithread_pipeline as cf


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    datasets = {
        "100_images": os.path.join(BASE_DIR, "..", "dataset", "images_100"),
        "5000_images": os.path.join(BASE_DIR, "..", "dataset", "images_5000")
    }

    RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    max_cpu = cpu_count()
    worker_counts = [2, 4, 8, 12, 16]
    worker_counts = [w for w in worker_counts if w <= max_cpu]

    print("--- CST435 Assignment 2: Parallel Image Processing ---")

    for name, path in datasets.items():

        if not os.path.exists(path):
            print(f"Skipping {name}: Path not found.")
            continue
        
        # Save processed images
        output_dir = os.path.join(RESULTS_DIR, name)
        seq.run_serial(path, output_dir, save=True)

        print("\n" + "=" * 50)
        print(f"DATASET: {name}")
        print("=" * 50)

        # Calculate serial baseline
        print("\n-- Sequential Baseline --")
        t_serial = seq.measure_serial(path)
        print(f"Serial Time: {t_serial:.4f}s")

        # Multiprocessing
        print("\n-- Multiprocessing Paradigm --\n")
        print(f"{'Workers':>8} | {'Time (s)':>10} | {'Speedup':>8} | {'Efficiency':>10}")
        print("-" * 46)

        for w in worker_counts:
            t_mp = mp.measure_mp(path, workers=w)
            speedup = t_serial / t_mp
            efficiency = speedup / w
            print(f"{w:>8} | {t_mp:>10.4f} | {speedup:>8.2f} | {efficiency:>10.2f}")

        # Multithreading
        print("\n-- Concurrent.Futures Paradigm --\n")
        print(f"{'Workers':>8} | {'Time (s)':>10} | {'Speedup':>8} | {'Efficiency':>10}")
        print("-" * 46)

        for w in worker_counts:
            t_cf = cf.measure_cf(path, workers=w)
            speedup = t_serial / t_cf
            efficiency = speedup / w
            print(f"{w:>8} | {t_cf:>10.4f} | {speedup:>8.2f} | {efficiency:>10.2f}")

    print("\n--Process complete.--")


if __name__ == "__main__":
    main()
