import json
import matplotlib.pyplot as plt

with open('discrete_uniform_series.json', 'r') as f:
    data = json.load(f)

theta = data['parameter']
sample_sizes = data['sample_sizes']
num_series = data['num_series']
series = data['series']

def empirical_cdf(sample, t):
    count = sum(1 for x in sample if x < t)
    return count / len(sample)

averaged_results = {}

print("Вычисление эмпирической функции распределения:")
print("=" * 60)

for size in sample_sizes:
    print(f"\nОбъем выборки n = {size}:")
    print("-" * 40)
    averaged_results[size] = {}
    for t in range(1, theta + 1):
        f_values = []

        for series_data in series:
            sample = series_data['samples'][str(size)]
            f_t = empirical_cdf(sample, t)
            f_values.append(f_t)
        avg_f_t = sum(f_values) / len(f_values)
        averaged_results[size][t] = avg_f_t
        print(f"  F({t}) = {avg_f_t:.6f}")

size = int(input("Введите размер выборки из набора {5, 10, 100, 200, 400, 600, 800, 1000}: "))

theoretical_values = [(t - 1) / theta for t in range(1, theta + 1)]
empirical_values = [averaged_results[size][t] for t in range(1, theta + 1)]
t_values = list(range(1, theta + 1))

plt.figure(figsize=(12, 6))
plt.plot(t_values, empirical_values, 'b-', linewidth=2, label='Эмпирическая F(t)')
plt.plot(t_values, theoretical_values, 'r--', linewidth=2, label='Теоретическая F(t)')

plt.xlabel('t')
plt.ylabel('F(t)')
plt.title(f'Сравнение эмпирической и теоретической функций распределения (n={size}, θ={theta})')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()