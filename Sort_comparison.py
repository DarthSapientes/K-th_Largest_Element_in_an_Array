# -------------------------
# Compare Quickselect, Full Sort, and Partial Sort (min-heap) empirically.
# -------------------------

import random
import time
import math
import statistics
import heapq
import numpy as np
import matplotlib.pyplot as plt
import gc
import sys
sys.setrecursionlimit(10**5) #in order to sidestep the RecursionError caused due to Python’s default recursion limit being 1000

# -------------------------
# Implementations
# -------------------------
def quickselect(A, k = int):
    if len(A) == 1:
        return A[0]

    pivot = A[-1]
    left = [x for x in A if x > pivot]
    right = [x for x in A if x <= pivot]
    right.remove(pivot)
    if k <= len(left):
        return quickselect(left, k)
    elif k == len(left) + 1:
        return pivot
    else:
        return quickselect(right, ((k - len(left)) - 1))

def kth_largest_fullsort(arr, k):
    # sorts descending and picks
    return sorted(arr, reverse=True)[k-1]

def kth_largest_heap(arr, k):
    # min-heap of size k -> return smallest of heap
    if k == 0:
        return None
    heap = arr[:k]
    heapq.heapify(heap)
    for x in arr[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap[0]

# -------------------------
# Experimental parameters
# -------------------------
random.seed(42)
np.random.seed(42)

n_list = [100, 500, 1000, 2000, 5000, 10000]
reps = 20   # repetitions per (n, k-scenario)
k_scenarios = ['k_small', 'k_middle', 'k_large', 'k_random']
k_small_fixed = 10

results = { 'quickselect': {s: [] for s in k_scenarios},
            'fullsort'   : {s: [] for s in k_scenarios},
            'heap'       : {s: [] for s in k_scenarios} }

# -------------------------
# Experiment loop
# -------------------------
for n in n_list:
    sizes = 1000 # not used; arr size = n
    # For each repetition we use a fresh random array
    for scenario in k_scenarios:
        times_qs = []
        times_fs = []
        times_hp = []
        for r in range(reps):
            # generate array of size n
            A = [random.randint(1, 10**6) for _ in range(n)]
            # choose k according to scenario
            if scenario == 'k_small':
                k = min(k_small_fixed, n)
            elif scenario == 'k_middle':
                k = max(1, n // 2)
            elif scenario == 'k_large':
                k = max(1, n - 10)
            else:  # random
                k = random.randint(1, n)

            # Quickselect (in-place) - measure time, give a copy to avoid cross-effects
            arr_qs = A.copy()
            gc.collect()
            t0 = time.perf_counter()
            _ = quickselect(arr_qs, k)
            t1 = time.perf_counter()
            times_qs.append(t1 - t0)

            # Full sort (sorted returns new list)
            arr_fs = A.copy()
            gc.collect()
            t0 = time.perf_counter()
            _ = kth_largest_fullsort(arr_fs, k)
            t1 = time.perf_counter()
            times_fs.append(t1 - t0)

            # Heap-based partial sort
            arr_hp = A.copy()
            gc.collect()
            t0 = time.perf_counter()
            _ = kth_largest_heap(arr_hp, k)
            t1 = time.perf_counter()
            times_hp.append(t1 - t0)

        # store averages (mean and std) for this n and scenario
        results['quickselect'][scenario].append((n, statistics.mean(times_qs), statistics.stdev(times_qs)))
        results['fullsort'][scenario].append((n, statistics.mean(times_fs), statistics.stdev(times_fs)))
        results['heap'][scenario].append((n, statistics.mean(times_hp), statistics.stdev(times_hp)))

# -------------------------
# Plotting results
# -------------------------
plt.style.use('ggplot')
colors = {'quickselect':'C0', 'fullsort':'C1', 'heap':'C2'}
markers = {'k_small':'o', 'k_middle':'s', 'k_large':'^', 'k_random':'x'}

for scenario in k_scenarios:
    plt.figure(figsize=(9,6))
    for algo in results:
        data = results[algo][scenario]
        ns = [t[0] for t in data]
        means = [t[1] for t in data]
        stds  = [t[2] for t in data]
        plt.errorbar(ns, means, yerr=stds, label=algo, color=colors[algo], marker=markers[scenario], capsize=3)

        # Fit linear and n log n for comparison
        # fit to y = a*n + b
        a, b = np.polyfit(ns, means, 1)
        # compute residuals for linear fit
        lin_pred = [a*x + b for x in ns]
        # also compute fit against n log n
        X = np.array([x * math.log(x+1) for x in ns])
        # fit y = c*X + d
        c, d = np.polyfit(X, means, 1)
        nlogn_pred = c*X + d


    plt.xlabel("n (array size)")
    plt.ylabel("Mean runtime (seconds)")
    plt.title(f"Runtime vs n — scenario: {scenario}")
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, which='both', ls='--', alpha=0.5)

    plt.show()
