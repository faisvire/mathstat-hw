import json
import matplotlib.pyplot as plt

with open('pareto_series.json', 'r') as f:
    data = json.load(f)
theta = data['parameter']
sample_sizes = data['sample_sizes']
num_series = data['num_series']
series = data['series']

def empirical_cdf(sample, t):
    count = sum(1 for x in sample if x < t)
    return count / len(sample)

averaged_results = {}

for size in sample_sizes:
    print(f"\nОбъем выборки n = {size}:")
    print("-" * 40)
    averaged_results[size] = {}
    all_values = []
    for series_data in series:
        sample = series_data['samples'][str(size)]
        all_values.extend(sample)
    unique_values = sorted(set(all_values))

    for t in unique_values:
        f_values = []
        for series_data in series:
            sample = series_data['samples'][str(size)]
            f_t = empirical_cdf(sample, t)
            f_values.append(f_t)
        avg_f_t = sum(f_values) / len(f_values)
        averaged_results[size][t] = avg_f_t
        print(f"  F({t:.4f}) = {avg_f_t:.6f}")

size = int(input("Введите размер выборки из набора {5, 10, 100, 200, 400, 600, 800, 1000}: "))

t_values = list(averaged_results[size].keys())
empirical_values = list(averaged_results[size].values())
theoretical_values = [1 - t ** (-theta) for t in t_values]

plt.figure(figsize=(12, 6))

# Ступенчатая функция для эмпирической ФР
plt.step(t_values, empirical_values, where='post', linewidth=2, label='Эмпирическая F(t)')

# Теоретическая ФР в тех же точках (без сглаживания)
plt.plot(t_values, theoretical_values, 'r-', linewidth=2, label='Теоретическая F(t)', markersize=4)

plt.xlabel('t')
plt.ylabel('F(t)')
plt.title(f'Сравнение эмпирической и теоретической функций распределения Парето (n={size}, θ={theta})')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()