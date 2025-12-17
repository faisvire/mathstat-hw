import json
import numpy as np

with open('discrete_uniform_series.json', 'r') as f:
    data = json.load(f)

theta = data['parameter']
sample_sizes = data['sample_sizes']
num_series = data['num_series']
series = data['series']


def empirical_cdf(sample, t):
    count = sum(1 for x in sample if x < t)
    return count / len(sample)

averaged_empirical = {}

for size in sample_sizes:
    averaged_empirical[size] = {}
    for t in range(1, theta + 1):
        f_values = []
        for series_data in series:
            sample = series_data['samples'][str(size)]
            f_t = empirical_cdf(sample, t)
            f_values.append(f_t)
        avg_f_t = sum(f_values) / len(f_values)
        averaged_empirical[size][t] = avg_f_t

print("Двухвыборочные статистики для дискретного равномерного распределения:")
print("=" * 70)

D_matrix = np.zeros((len(sample_sizes), len(sample_sizes)))

for i, n in enumerate(sample_sizes):
    for j, m in enumerate(sample_sizes):
        if n < m:
            sup_diff = 0
            for t in range(1, theta + 1):
                diff = abs(averaged_empirical[n][t] - averaged_empirical[m][t])
                if diff > sup_diff:
                    sup_diff = diff
            D_mn = np.sqrt((n * m) / (m + n)) * sup_diff
            D_matrix[i, j] = D_mn

            print(f"D({n},{m}) = {D_mn:.6f}")

print("\nМатрица двухвыборочных статистик:")
print(" " * 8, end="")
for size in sample_sizes:
    print(f"{size:>8}", end="")
print()

for i, n in enumerate(sample_sizes):
    print(f"{n:>8}", end="")
    for j, m in enumerate(sample_sizes):
        if n < m:
            print(f"{D_matrix[i, j]:>8.4f}", end="")
        else:
            print(f"{'':>8}", end="")
    print()