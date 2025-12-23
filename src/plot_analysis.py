import os
import numpy as np
import matplotlib.pyplot as plt


def plot_analysis(results, output_dir="../results/graphs"):
    """
    Generate merged professional graphs from experiment results.
    """

    os.makedirs(output_dir, exist_ok=True)

    # ============================================
    # 1. Execution Time (Merged)
    # ============================================
    plt.figure(figsize=(10, 6))

    for dataset, data in results.items():
        workers = np.array(data["workers"])
        mp_times = np.array(data["multiprocessing"])
        mt_times = np.array(data["multithreading"])

        plt.plot(workers, mp_times, "o-", label=f"{dataset} – MP")
        plt.plot(workers, mt_times, "s--", label=f"{dataset} – MT")

    plt.xlabel("Number of Workers")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time vs Workers (All Datasets)")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.savefig(f"{output_dir}/merged_execution_time.png", dpi=300)
    plt.close()

    # ============================================
    # 2. Speedup (Merged)
    # ============================================
    plt.figure(figsize=(10, 6))

    for dataset, data in results.items():
        workers = np.array(data["workers"])
        serial = data["serial"]

        mp_speedup = serial / np.array(data["multiprocessing"])
        mt_speedup = serial / np.array(data["multithreading"])

        plt.plot(workers, mp_speedup, "o-", label=f"{dataset} – MP")
        plt.plot(workers, mt_speedup, "s--", label=f"{dataset} – MT")

    plt.xlabel("Number of Workers")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Workers (All Datasets)")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.savefig(f"{output_dir}/merged_speedup.png", dpi=300)
    plt.close()

    # ============================================
    # 3. Efficiency (Merged)
    # ============================================
    plt.figure(figsize=(10, 6))

    for dataset, data in results.items():
        workers = np.array(data["workers"])
        serial = data["serial"]

        mp_eff = (serial / np.array(data["multiprocessing"])) / workers
        mt_eff = (serial / np.array(data["multithreading"])) / workers

        plt.plot(workers, mp_eff, "o-", label=f"{dataset} – MP")
        plt.plot(workers, mt_eff, "s--", label=f"{dataset} – MT")

    plt.xlabel("Number of Workers")
    plt.ylabel("Efficiency")
    plt.title("Parallel Efficiency (All Datasets)")
    plt.ylim(0, 1.1)
    plt.legend()
    plt.grid(alpha=0.3)

    plt.savefig(f"{output_dir}/merged_efficiency.png", dpi=300)
    plt.close()

    # ============================================
    # 4. MP vs MT Performance Ratio (Optional)
    # ============================================
    plt.figure(figsize=(10, 6))

    for dataset, data in results.items():
        workers = np.array(data["workers"])
        ratio = np.array(data["multiprocessing"]) / np.array(data["multithreading"])

        plt.plot(workers, ratio, "o-", label=dataset)

    plt.axhline(1, linestyle="--", color="black", label="Equal Performance")

    plt.xlabel("Number of Workers")
    plt.ylabel("MP / MT Time Ratio")
    plt.title("Multiprocessing vs Multithreading Performance Ratio")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.savefig(f"{output_dir}/mp_vs_mt_ratio.png", dpi=300)
    plt.close()

    print("All analysis graphs saved successfully")
