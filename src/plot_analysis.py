import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Save plot to file
def save_plot(filename, folder):
    os.makedirs(folder, exist_ok=True)
    plt.savefig(os.path.join(folder, filename), dpi=300, bbox_inches="tight")
    plt.close()

# Plot graph
def plot_graph(workers, y1, y2, label1, label2, ylabel, title, filename, outdir, color1, color2):
    plt.figure()
    plt.plot(workers, y1, "o-",color= color1, label=label1)
    plt.plot(workers, y2, "o-", color= color2, label=label2)
    plt.xlabel("Number of Workers")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    save_plot(filename, outdir)

# Generate all performance graphs
def plot_analysis(results):

    # Set directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, "..", "results", "graphs")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    for dataset, data in results.items():
        workers = data["workers"]

        # Extract multiprocessing results
        mp = data["multiprocessing"]
        mp_execution = [t for t, _, _ in mp]
        sp_mp = [s for _, s, _ in mp]
        ef_mp = [e for _, _, e in mp]

        # Extract multithreading results
        mt = data["multithreading"]
        mt_execution = [t for t, _, _ in mt]
        sp_mt = [s for _, s, _ in mt]
        ef_mt = [e for _, _, e in mt]

        # Extract Amdahl predictions
        amdahl_mp = data["amdahl_mp"]
        amdahl_mt = data["amdahl_mt"]
        
        # Create dataset output folder
        dataset_dir = os.path.join(RESULTS_DIR, dataset)
        os.makedirs(dataset_dir, exist_ok=True)

        # -------- Execution Time --------
        plot_graph(
            workers,
            mp_execution,
            mt_execution,
            "Multiprocessing",
            "Multithreading",
            "Execution Time (s)",
            "Multiprocessing Execution Time vs MultiThreading Execution Time ",
            "mp_execution_time_vs_mt_execution.png",
            os.path.join(dataset_dir, "Execution Time"),
            "red",
            "blue"
        )

        plot_graph(
            workers,
            mp_execution,
            amdahl_mp["execution_time"],
            "Multiprocessing",
            "Amdahl",
            "Execution Time (s)",
            "Multiprocessing Execution Time vs Amdahl Execution Time",
            "mp_execution_time_vs_amdahl.png",
            os.path.join(dataset_dir, "Execution Time"),
            "red",
            "green"
        )

        plot_graph(
            workers,
            mt_execution,
            amdahl_mt["execution_time"],
            "MultiThreading",
            "Amdahl",
            "Execution Time (s)",
            "Multithreading Execution Time vs Amdahl Execution Time",
            "mt_execution_time_vs_amdahl.png",
            os.path.join(dataset_dir, "Execution Time"),
            "blue",
            "green"
        )

        # -------- Speedup --------
        plot_graph(
            workers,
            sp_mp,
            sp_mt,
            "Multiprocessing",
            "Multithreading",
            "SpeedUp",
            "Multiprocessing Speedup vs MultiThreading Speedup",
            "mp_speedup_vs_mt_speedup.png",
            os.path.join(dataset_dir, "SpeedUp"),
            "red",
            "blue"
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
            os.path.join(dataset_dir, "Speedup"),
            "red",
            "green"
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
            os.path.join(dataset_dir, "SpeedUp"),
            "blue",
            "green"
        )

        # -------- Efficiency --------
        plot_graph(
            workers,
            ef_mp,
            ef_mt,
            "Multiprocessing",
            "Multithreading",
            "Efficiency",
            "Multiprocessing Efficiency vs Multithreading Efficiency ",
            "mp_efficiency_vs_mt_efficiency.png",
            os.path.join(dataset_dir, "Efficiency"),
            "red",
            "blue"
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
            os.path.join(dataset_dir, "Efficiency"),
            "red",
            "green"
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
            os.path.join(dataset_dir, "Efficiency"),
            "blue",
            "green"
        )

    print("All graphs generated using precomputed Amdahl predictions.")
