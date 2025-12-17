import json
import matplotlib.pyplot as plt
import numpy as np

with open('pareto_series.json', 'r') as f:
    data = json.load(f)

theta = data['parameter']
sample_sizes = data['sample_sizes']
num_series = data['num_series']
series = data['series']

def calculate_combined_histogram(size):
    all_values = []
    for series_data in series:
        sample = series_data['samples'][str(size)]
        all_values.extend(sample)
    total_observations = len(all_values)
    num_bins = 15
    counts, bin_edges = np.histogram(all_values, bins=num_bins)
    bin_widths = np.diff(bin_edges)
    bin_midpoints = (bin_edges[:-1] + bin_edges[1:]) / 2
    density = counts / (total_observations * bin_widths)
    return bin_midpoints, density, bin_edges, bin_widths, counts, total_observations
def pareto_density(x, theta):
    return theta * x ** (-(theta + 1))

size = int(input("Введите размер выборки из набора {5, 10, 100, 200, 400, 600, 800, 1000}: "))
bin_midpoints, empirical_density, bin_edges, bin_widths, counts, total_obs = calculate_combined_histogram(size)
plt.figure(figsize=(12, 6))
plt.bar(bin_midpoints, empirical_density, width=bin_widths,
        alpha=0.5, color='lightblue', edgecolor='blue', linewidth=1,
        label=f'Гистограмма (по {total_obs} наблюдениям)')
plt.plot(bin_midpoints, empirical_density, 'bo-', linewidth=2, markersize=6,
         label='Полигон частот')
x_smooth = np.linspace(min(bin_midpoints), max(bin_midpoints), 1000)
y_smooth = [pareto_density(x, theta) for x in x_smooth]
plt.plot(x_smooth, y_smooth, 'r-', linewidth=2, label='Теоретическая плотность')
plt.xlabel('Значение x')
plt.ylabel('Плотность вероятности')
plt.title(f'Сравнение гистограммы и полигона частот по всем выборкам с плотностью для распределения Парето (n={size}, θ={theta})')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
