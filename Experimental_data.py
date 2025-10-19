import random
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.setrecursionlimit(10**5)

#------------------------------
# Quickselect implementation
# ------------------------------

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

# -----------------------------
# Experiment setup
# -----------------------------
Ns = [100, 500, 1000, 2000, 5000, 10000]
times_sorted = []
times_nearly_sorted = []
times_random = []

for n in Ns:
    k = n // 2  # median element
    trials = 10

    t_sorted = 0
    t_near = 0
    t_rand = 0

    for _ in range(trials):
        # Case 1: Sorted array (worst case)
        A_sorted = list(range(n))
        start = time.perf_counter()
        quickselect(A_sorted.copy(), k)
        t_sorted += time.perf_counter() - start

        # Case 2: Nearly sorted (1% elements swapped)
        A_near = A_sorted.copy()
        for _ in range(max(1, n // 100)):
            i, j = random.sample(range(n), 2)
            A_near[i], A_near[j] = A_near[j], A_near[i]
        start = time.perf_counter()
        quickselect(A_near.copy(), k)
        t_near += time.perf_counter() - start

        # Case 3: Random array
        A_rand = [random.randint(1, 10 ** 5) for _ in range(n)]
        start = time.perf_counter()
        quickselect(A_rand.copy(), k)
        t_rand += time.perf_counter() - start

    times_sorted.append(t_sorted / trials)
    times_nearly_sorted.append(t_near / trials)
    times_random.append(t_rand / trials)

# -----------------------------
# Plot results
# -----------------------------
plt.style.use('bmh')
plt.figure(figsize=(10, 6))
plt.plot(Ns, times_sorted, 'o-', label='Sorted (Worst Case)')
plt.plot(Ns, times_nearly_sorted, 's-', label='Nearly Sorted')
plt.plot(Ns, times_random, '^-', label='Random (Average Case)')

plt.xlabel("Array Size (n)")
plt.ylabel("Average Runtime (seconds)")
plt.title("Runtime of Quickselect under Different Input Conditions")
plt.legend()
plt.grid(True)
plt.show()

