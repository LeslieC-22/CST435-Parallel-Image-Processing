import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ==================================================
# Utility helpers
# ==================================================
def save_plot(filename, folder):
    os.makedirs(folder, exist_ok=True)
    plt.savefig(os.path.join(folder, filename), dpi=300, bbox_inches="tight")
    plt.close()


def compute_speedup(serial, times):
    return [serial / t for t in times]


def compute_efficiency(speedups, workers):
    return [s / w for s, w in zip(speedups, workers)]


# ==================================================
# Plot functions
# ==================================================

def plot_graph(workers, y1, y2, label1, label2, ylabel, title, filename, outdir):
    plt.figure()
    plt.plot(workers, y1, "o-", label=label1)
    plt.plot(workers, y2, "s--", label=label2)
    plt.xlabel("Number of Workers")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    save_plot(filename, outdir)

# ==================================================
# MAIN ENTRY
# ==================================================
def plot_analysis(results):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, "..", "results", "graphs")

    os.makedirs(RESULTS_DIR, exist_ok=True)

    for dataset, data in results.items():

        workers = data["workers"]
        serial = data["serial"]

        # Measured results
        mp_times = data["multiprocessing"]
        mt_times = data["multithreading"]

        sp_mp = compute_speedup(serial, mp_times)
        sp_mt = compute_speedup(serial, mt_times)

        ef_mp = compute_efficiency(sp_mp, workers)
        ef_mt = compute_efficiency(sp_mt, workers)

        # Amdahl predictions (ALREADY COMPUTED)
        amdahl_mp = data["amdahl_mp"]
        amdahl_mt = data["amdahl_mt"]

        dataset_dir = os.path.join(RESULTS_DIR, dataset)
        os.makedirs(dataset_dir, exist_ok=True)

        # ==================================================
        # Execution Time
        # ================================================== 

        plot_graph(
            workers,
            mp_times,
            mt_times,
            "Multiprocessing",
            "Multithreading",
            "Execution Time (s)",
            "Multiprocessing Execution Time vs MultiThreading Execution Time ",
            "mp_execution_time_vs_mt_execution.png",
            os.path.join(dataset_dir, "Execution Time")
        )

        plot_graph(
            workers,
            mp_times,
            amdahl_mp["execution_time"],
            "Multiprocessing",
            "Amdahl",
            "Execution Time (s)",
            "Multiprocessing Execution Time vs Amdahl Execution Time",
            "mp_execution_time_vs_amdahl.png",
            os.path.join(dataset_dir, "Execution Time")
        )

        plot_graph(
            workers,
            mt_times,
            amdahl_mt["execution_time"],
            "MultiThreading",
            "Amdahl",
            "Execution Time (s)",
            "Multithreading Execution Time vs Amdahl Execution Time",
            "mt_execution_time_vs_amdahl.png",
            os.path.join(dataset_dir, "Execution Time")
        )

        # ==================================================
        # SpeedUp
        # ================================================== 

        plot_graph(
            workers,
            sp_mp,
            sp_mt,
            "Multiprocessing",
            "Multithreading",
            "SpeedUp",
            "Multiprocessing Speedup vs MultiThreading Speedup",
            "mp_speedup_vs_mt_speedup.png",
            os.path.join(dataset_dir, "SpeedUp")
        )

        plot_graph(
            workers,
            sp_mp,
            amdahl_mp["speedup"],
            "Multiprocessing",
            "Amdahl",
            "Speedup",
            "Multiprocessing Speedup vs Amdahl Speedup",
            "mp_speedup_vs_amdahl.png",
            os.path.join(dataset_dir, "Speedup")
        )
        plot_graph(
            workers,
            sp_mt,
            amdahl_mt["speedup"],
            "MultiThreading",
            "Amdahl",
            "Speedup",
            "Multithreading Speedup vs Amdahl Speedup",
            "mt_speedup_vs_amdahl.png",
            os.path.join(dataset_dir, "SpeedUp")
        )

        # ==================================================
        # Efficiency
        # ================================================== 
        plot_graph(
            workers,
            ef_mp,
            ef_mt,
            "Multiprocessing",
            "Multithreading",
            "Efficiency",
            "Multiprocessing Efficiency vs Multithreading Efficiency ",
            "mp_efficiency_vs_mt_efficiency.png",
            os.path.join(dataset_dir, "Efficiency")
        )

        plot_graph(
            workers,
            ef_mp,
            amdahl_mp["efficiency"],
            "Multiprocessing",
            "Amdahl",
            "Efficiency",
            "Multiprocessing Efficiency vs Amdahl Efficiency",
            "mp_efficiency_vs_amdahl.png",
            os.path.join(dataset_dir, "Efficiency")
        )

        plot_graph(
            workers,
            ef_mt,
            amdahl_mt["efficiency"],
            "MultiThreading",
            "Amdahl",
            "Efficiency",
            "Multithreading Efficiency vs Amdahl Efficiency",
            "mt_efficiency_vs_amdahl.png",
            os.path.join(dataset_dir, "Efficiency")
        )

    print("All graphs generated using precomputed Amdahl predictions.")
