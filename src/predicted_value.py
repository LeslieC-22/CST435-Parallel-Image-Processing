def estimate_parallel_fraction(serial_time, parallel_time, workers):
    """
    Estimate parallel fraction (P) using Amdahl's Law.
    """
    speedup = serial_time / parallel_time

    if workers <= 1 or speedup <= 1:
        return 0.0

    P = (1 - (1 / speedup)) / (1 - (1 / workers))
    return max(0.0, min(P, 1.0))


def amdahl_speedup(P, workers):
    return 1 / (P + (1 - P) / workers)


def amdahl_execution_time(serial_time, speedup):
    return serial_time / speedup


def amdahl_efficiency(speedup, workers):
    return speedup / workers


def compute_amdahl_predictions(serial_time, worker_list, measured_times):
    """
    Compute and PRINT Amdahl's Law results.
    """

    # Determine best observed configuration
    best_index = measured_times.index(min(measured_times))
    best_workers = worker_list[best_index]
    best_time = measured_times[best_index]

    # Estimate parallel fraction
    P = estimate_parallel_fraction(serial_time, best_time, best_workers)

    print("\n================ Amdahl's Law Analysis ================")
    print(f"Estimated Parallel Fraction (P): {P:.4f}")
    print("-------------------------------------------------------")
    print(f"{'Workers':>8} | {'Exec Time':>12} | {'SpeedUp':>10} | {'Efficiency':>11}")
    print("-" * 55)

    results = {
        "parallel_fraction": P,
        "speedup": [],
        "execution_time": [],
        "efficiency": []
    }

    for w in worker_list:
        s = amdahl_speedup(P, w)
        t = amdahl_execution_time(serial_time, s)
        e = amdahl_efficiency(s, w)

        results["execution_time"].append(t)
        results["speedup"].append(s)
        results["efficiency"].append(e)

        print(f"{w:>8} | {t:>12.3f} | {s:>10.3f} | {e:>11.3f}")

    print("=======================================================\n")

    return results
