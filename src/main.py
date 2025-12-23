import os
import math
from multiprocessing import cpu_count

# Execution paradigms
import serial_pipeline as seq
import multiprocessing_pipeline as mp
import multithread_pipeline as cf

# Plotting graphs
import plot_analysis


# ==================================================
# Formatting helpers
# ==================================================
WIDTH = 60

def print_title(title):
    print("\n" + "=" * WIDTH)
    print(title.center(WIDTH))
    print("=" * WIDTH)

def print_section(title):
    print("\n" + title)
    print("-" * WIDTH)

def print_table_header():
    print(f"{'Workers':>8} | {'Time (s)':>10} | {'Speedup':>8} | {'Efficiency':>10}")
    print("-" * WIDTH)


# ==================================================
# Main experiment
# ==================================================
def run_experiments():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    datasets = {
        "100_images": os.path.join(BASE_DIR, "..", "dataset", "images_100"),
        "5000_images": os.path.join(BASE_DIR, "..", "dataset", "images_5000")
    }

    # Worker configuration (power-of-two scaling)
    max_cpu = cpu_count()
    max_exp = int(math.log2(max_cpu))
    worker_counts = [2 ** x for x in range(1, max_exp + 1)]
    worker_counts.append(max_cpu * 2)  # oversubscription

    print_title("CST435 ASSIGNMENT 2: PARALLEL IMAGE PROCESSING")
    print(f"Logical CPUs detected : {max_cpu}")
    print(f"Worker configurations : {worker_counts}")

    all_results = {}

    for dataset_name, dataset_path in datasets.items():

        if not os.path.exists(dataset_path):
            print(f"[WARNING] Dataset not found: {dataset_name}")
            continue

        print_title(f"DATASET: {dataset_name}")

        # Serial baseline
        print_section("SEQUENTIAL BASELINE")
        t_serial = seq.measure_serial(dataset_path)
        print(f"Execution Time : {t_serial:.4f} seconds")

        mp_times, mt_times = [], []

        # Multiprocessing
        print_section("MULTIPROCESSING RESULTS")
        print_table_header()
        for w in worker_counts:
            t = mp.measure_mp(dataset_path, workers=w)
            mp_times.append(t)
            print(f"{w:>8} | {t:>10.4f} | {t_serial/t:>8.2f} | {(t_serial/t)/w:>10.2f}")

        # Multithreading
        print_section("MULTITHREADING RESULTS")
        print_table_header()
        for w in worker_counts:
            t = cf.measure_cf(dataset_path, workers=w)
            mt_times.append(t)
            print(f"{w:>8} | {t:>10.4f} | {t_serial/t:>8.2f} | {(t_serial/t)/w:>10.2f}")

        # Store results (NO plotting here)
        all_results[dataset_name] = {
            "workers": worker_counts,
            "serial": t_serial,
            "multiprocessing": mp_times,
            "multithreading": mt_times
        }

    print_title("PROCESS COMPLETED SUCCESSFULLY")
    return all_results


# ==================================================
# Entry point
# ==================================================
if __name__ == "__main__":
    
    results = run_experiments()
    plot_analysis.plot_analysis(results)
