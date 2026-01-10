# Estimate parallel fraction (P) using Amdahl's Law
def estimate_parallel_fraction(serial_time, parallel_time, workers):
    # Calculate speedup
    speedup = serial_time / parallel_time

    if workers <= 1 or speedup <= 1:
        return 0.0

    # Compute parallel fraction P
    P = (1 - (1 / speedup)) / (1 - (1 / workers))
    return max(0.0, min(P, 1.0))

# Calculate theoretical speedup using Amdahl's Law
def amdahl_speedup(P, workers):
    return 1 / (P + (1 - P) / workers)

# Calculate execution time based on speedup
def amdahl_execution_time(serial_time, speedup):
    return serial_time / speedup

# Calculate efficiency based on speedup
def amdahl_efficiency(speedup, workers):
    return speedup / workers

# Compute and display Amdahl's Law predictions
def compute_amdahl_predictions(serial_time, worker_list, measured_times):

    # Determine best observed configuration
    best_index = measured_times.index(min(measured_times))
    best_workers = worker_list[best_index]
    best_time = measured_times[best_index]

    # Estimate parallel fraction
    P = estimate_parallel_fraction(serial_time, best_time, best_workers)

    # Print Amdahl's Law's Result
    print("\n================ Amdahl's Law Analysis ================")
    print(f"Estimated Parallel Fraction (P): {P:.4f}")
    print("-------------------------------------------------------")
    print(f"{'Workers':>8} | {'Exec Time (s)':>12} | {'SpeedUp':>10} | {'Efficiency':>11}")
    print("-" * 55)

    # Store results for plotting
    results = {
        "parallel_fraction": P,
        "speedup": [],
        "execution_time": [],
        "efficiency": []
    }

    # Compute predictions for each worker count
    for w in worker_list:
        s = round(amdahl_speedup(P, w),2)
        t = round(amdahl_execution_time(serial_time, s),2)
        e = round(amdahl_efficiency(s, w),2)

        results["execution_time"].append(t)
        results["speedup"].append(s)
        results["efficiency"].append(e)

        print(f"{w:>8} | {t:>12.2f} | {s:>10.2f} | {e:>11.2f}")

    print("=======================================================\n")

    return results
