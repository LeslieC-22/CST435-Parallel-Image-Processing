import os
import matplotlib

# Disable interactive backend (no pop-ups)
matplotlib.use("Agg")

import matplotlib.pyplot as plt


# ==================================================
# Helper calculations
# ==================================================
def compute_speedup(serial_time, parallel_times):
    return [serial_time / t for t in parallel_times]


def compute_efficiency(speedups, workers):
    return [s / w for s, w in zip(speedups, workers)]


# ==================================================
# Save-only helper
# ==================================================
def save_only(filename, graphs_dir):
    os.makedirs(graphs_dir, exist_ok=True)
    path = os.path.join(graphs_dir, filename)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


# ==================================================
# Combined execution-time plot (ONLY ONE)
# ==================================================
def plot_combined_execution_time(results, graphs_dir):
    """
    Combined execution-time graph for both datasets.
    This is safe because execution time is absolute.
    """

    plt.figure()

    for dataset_name, data in results.items():
        workers = data["workers"]
        mp_times = data["multiprocessing"]
        mt_times = data["multithreading"]

        plt.plot(
            workers,
            mp_times,
            marker="o",
            linestyle="-",
            label=f"MP - {dataset_name}"
        )

        plt.plot(
            workers,
            mt_times,
            marker="s",
            linestyle="--",
            label=f"MT - {dataset_name}"
        )

    plt.xlabel("Number of Workers")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time vs Workers (100 vs 5000 Images)")
    plt.legend()
    plt.grid(True)

    save_only("combined_execution_time.png", graphs_dir)


# ==================================================
# Per-dataset speedup & efficiency plots
# ==================================================
def plot_speedup(workers, sp_mp, sp_mt, graphs_dir):
    plt.figure()
    plt.plot(workers, sp_mp, marker="o", label="Multiprocessing")
    plt.plot(workers, sp_mt, marker="s", label="Concurrent.Futures")
    plt.xlabel("Number of Workers")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Workers")
    plt.legend()
    plt.grid(True)

    save_only("speedup.png", graphs_dir)


def plot_efficiency(workers, ef_mp, ef_mt, graphs_dir):
    plt.figure()
    plt.plot(workers, ef_mp, marker="o", label="Multiprocessing")
    plt.plot(workers, ef_mt, marker="s", label="Concurrent.Futures")
    plt.xlabel("Number of Workers")
    plt.ylabel("Efficiency")
    plt.title("Efficiency vs Workers")
    plt.legend()
    plt.grid(True)

    save_only("efficiency.png", graphs_dir)


# ==================================================
# Main plotting entry
# ==================================================
def plot_analysis(results):
    """
    Expected results structure:
    {
        dataset_name: {
            "workers": [...],
            "serial": float,
            "multiprocessing": [...],
            "multithreading": [...]
        }
    }
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_GRAPHS_DIR = os.path.join(BASE_DIR, "..", "results", "graphs")

    # -------- Combined execution-time graph --------
    plot_combined_execution_time(results, BASE_GRAPHS_DIR)

    # -------- Dataset-specific speedup & efficiency --------
    for dataset_name, data in results.items():

        dataset_graphs_dir = os.path.join(BASE_GRAPHS_DIR, dataset_name)

        workers = data["workers"]
        serial_time = data["serial"]
        mp_times = data["multiprocessing"]
        mt_times = data["multithreading"]

        # Dataset-specific baseline calculations
        sp_mp = compute_speedup(serial_time, mp_times)
        sp_mt = compute_speedup(serial_time, mt_times)

        ef_mp = compute_efficiency(sp_mp, workers)
        ef_mt = compute_efficiency(sp_mt, workers)

        plot_speedup(workers, sp_mp, sp_mt, dataset_graphs_dir)
        plot_efficiency(workers, ef_mp, ef_mt, dataset_graphs_dir)
