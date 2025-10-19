import random
import time
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------
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

def randomized_quickselect(A, k = int): 
    if len(A) == 1:
        return A[0]

    pivot = A[random.randint(1, len(A)-1)]
    left = [x for x in A if x > pivot]
    right = [x for x in A if x <= pivot]
    right.remove(pivot)
    if k <= len(left):
        return randomized_quickselect(left, k)
    elif k == len(left) + 1:
        return pivot
    else:
        return randomized_quickselect(right, ((k - len(left)) - 1))

# ------------------------------
# Experimental setup
# ------------------------------

Ns = range(1, 101)     # n = 1 to 100
avg_times = []         # store average runtimes t_n
worst_times = []       # store worst runtime of t_n

for n in Ns:
    total_time = 0.0
    worst_time = 0.0
    size = 100 * n     # each array has 100 * n elements

    for i in range(20):  # 20 random arrays per n
        A = [random.randint(1, 10**6) for _ in range(size)]
        k = random.randint(1, size)

        start = time.perf_counter()
        quickselect(A.copy(), k)
        end = time.perf_counter()

        total_time += (end - start)
        if worst_time < (end - start):
            worst_time = (end - start)

    t_n = total_time / 20
    avg_times.append(t_n)
    worst_times.append(worst_time)

# ------------------------------
# Plotting
# ------------------------------
#Linear Fit Curve
# ------------------------------
plt.figure(figsize=(10, 6))
plt.scatter(Ns, avg_times, color='blue', label='Measured avg runtime', alpha=0.7)

# Linear best-fit curve
lin_coeffs = np.polyfit(Ns, avg_times, 1)
fit_line = np.poly1d(lin_coeffs)
plt.plot(Ns, fit_line(Ns), color='red', label=f'Best linear fit: y = {lin_coeffs[0]:.2e}x + {lin_coeffs[1]:.2e}')

plt.xlabel('n (array size factor, each array = 100*n elements)')
plt.ylabel('Average runtime (seconds)')
plt.title('Quickselect runtime vs n (averaged over 20 trials)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# ------------------------------
# Quadratic bound computation
# ------------------------------

Ns_array = np.array(list(Ns))
times_array = np.array(worst_times)
C = max(times_array / (Ns_array**2))   # empirical constant upper bound
quad_bound = C * (Ns_array**2)

# ------------------------------
# Plot worst-case runtimes and quadratic bound
# ------------------------------

plt.style.use('bmh')
plt.figure(figsize=(10, 6))

plt.scatter(Ns_array, times_array, color='tab:blue', label='Measured worst runtime $T(n)$')
plt.plot(Ns_array, quad_bound, color='tab:red', linestyle='--', label=f'Quadratic bound $C n^2$ (C={C:.2e})')

plt.xlabel("n (scaled array size = 100×n)")
plt.ylabel("Runtime (seconds)")
plt.title("Empirical Quadratic Bound on Quickselect Worst-Case Runtime")
plt.legend()
plt.grid(True)

plt.show()
