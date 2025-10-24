import json
import matplotlib.pyplot as plt

with open('discrete_uniform_series.json', 'r') as f:
    data = json.load(f)

theta = data['parameter']
sample_sizes = data['sample_sizes']
num_series = data['num_series']
series = data['series']

def calculate_averaged_frequencies(size):
    frequency_sum = {t: 0 for t in range(1, theta + 1)}
    for series_data in series:
        sample = series_data['samples'][str(size)]
        sample_freq = {}
        for t in range(1, theta + 1):
            count = sample.count(t)
            sample_freq[t] = count / len(sample)  # относительная частота
        for t in range(1, theta + 1):
            frequency_sum[t] += sample_freq.get(t, 0)

    averaged_frequencies = {t: frequency_sum[t] / num_series for t in range(1, theta + 1)}
    return averaged_frequencies

theoretical_density = {t: 1 / theta for t in range(1, theta + 1)}
size = int(input("Введите размер выборки из набора {5, 10, 100, 200, 400, 600, 800, 1000}: "))
averaged_freq = calculate_averaged_frequencies(size)
t_values = list(range(1, theta + 1))
empirical_freq_values = [averaged_freq[t] for t in t_values]
theoretical_density_values = [theoretical_density[t] for t in t_values]

plt.figure(figsize=(12, 6))

plt.plot(t_values, empirical_freq_values, 'bo-', linewidth=2, markersize=3, label='Усредненный полигон частот')

plt.stem(t_values, theoretical_density_values, linefmt='r-', markerfmt='ro', basefmt=' ', label='Теоретическая плотность')
plt.gca().get_lines()[1].set_markersize(2)

plt.xlabel('Значение t')
plt.ylabel('Вероятность/Частота')
plt.title(f'Сравнение усредненного полигона частот и теоретической плотности (n={size}, θ={theta})')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
