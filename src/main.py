import os
import math
from multiprocessing import cpu_count

# Import execution pipelines
import serial_pipeline as seq
import multiprocessing_pipeline as mp
import multithread_pipeline as cf
import predicted_value as amdahl

# Import plotting module
import plot_analysis

WIDTH = 60

# Print main title
def print_title(title):
    print("\n" + "=" * WIDTH)
    print(title.center(WIDTH))
    print("=" * WIDTH)

# Print section header
def print_section(title):
    print("\n" + title)
    print("-" * WIDTH)

# Print table header
def print_table_header():
    print(f"{'Workers':>8} | {'Exec Time (s)':>10} | {'Speedup':>8} | {'Efficiency':>10}")
    print("-" * WIDTH)

# Run all experiments
def run_experiments():

    # Set base and results directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Dataset paths
    datasets = {
        "100_images": os.path.join(BASE_DIR, "..", "dataset", "images_100"),
        "5000_images": os.path.join(BASE_DIR, "..", "dataset", "images_5000")
    }

    # Determine worker counts
    max_cpu = cpu_count()
    max_exp = int(math.log2(max_cpu))
    worker_counts = [2 ** x for x in range(1, max_exp + 1)]

    if max_cpu not in worker_counts:
        worker_counts.append(max_cpu)

    worker_counts.append(max_cpu * 2)
    worker_counts = sorted(set(worker_counts))

    # Print experiment info
    print_title("CST435 ASSIGNMENT 2: PARALLEL IMAGE PROCESSING")
    print(f"Logical CPUs detected : {max_cpu}")
    print(f"Worker configurations : {worker_counts}")

    all_results = {}

    # Run experiments for each dataset
    for dataset_name, dataset_path in datasets.items():

        if not os.path.exists(dataset_path):
            print(f"[WARNING] Dataset not found: {dataset_name}")
            continue

        # Save processed images for sequential version
        output_dir = os.path.join(RESULTS_DIR, dataset_name)
        seq.run_serial(dataset_path, output_dir, save=True)

        print_title(f"DATASET: {dataset_name}")

        # Run sequential baseline
        print_section("SEQUENTIAL BASELINE")
        t_serial = seq.measure_serial(dataset_path)
        print(f"Execution Time : {t_serial:.4f} seconds")

        mp_times, mt_times = [], []

        # Run multiprocessing tests
        print_section("MULTIPROCESSING RESULTS")
        print_table_header()
        for w in worker_counts:
            t = mp.measure_mp(dataset_path, workers=w)
            s = t_serial / t
            e = s / w
            mp_times.append((t, s, e))
            print(f"{w:>8} | {t:>10.2f} | {s:>8.2f} | {e:>10.2f}")

        # Compute Amdahl predictions for multiprocessing
        amdahl_mp = amdahl.compute_amdahl_predictions(
            serial_time=t_serial,
            worker_list=worker_counts,
            measured_times=[t for t, _, _ in mp_times]
        )

        # Run multithreading tests
        print_section("MULTITHREADING RESULTS")
        print_table_header()
        for w in worker_counts:
            t = cf.measure_cf(dataset_path, workers=w)
            s = t_serial / t
            e = s / w
            mt_times.append((t, s, e))
            print(f"{w:>8} | {t:>10.2f} | {s:>8.2f} | {e:>10.2f}")

        # Compute Amdahl predictions for multithreading
        amdahl_mt = amdahl.compute_amdahl_predictions(
            serial_time=t_serial,
            worker_list=worker_counts,
            measured_times=[t for t, _, _ in mt_times]
        )

        # Store results for plotting
        all_results[dataset_name] = {
            "workers": worker_counts,
            "serial": t_serial,
            "multiprocessing": mp_times,
            "multithreading": mt_times,
            "amdahl_mp": amdahl_mp,
            "amdahl_mt": amdahl_mt
        }

    # Print completion message
    print_title("PROCESS COMPLETED SUCCESSFULLY")
    return all_results


# Program entry point
if __name__ == "__main__":

    # Run experiments
    results = run_experiments()

    # Generate graphs
    plot_analysis.plot_analysis(results)
