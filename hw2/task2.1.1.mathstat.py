import json
import math
import random

def generate_discrete_uniform_sample(theta, sample_size):
    sample = []
    for _ in range(sample_size):
        gamma = random.uniform(0, 1)
        mu_gamma = math.floor(gamma * theta) + 1
        sample.append(mu_gamma)
    return sample

theta = 121
sample_sizes = [5, 10, 100, 200, 400, 600, 800, 1000]
num_series = 5
all_series = []

for series_num in range(num_series):
    print(f"\nГенерация серии {series_num + 1}:")
    series_data = {
        "series_number": series_num + 1,
        "samples": {}
    }
    cumulative_sample = []
    for size in sample_sizes:
        additional_size = size - len(cumulative_sample)
        if additional_size > 0:
            new_elements = generate_discrete_uniform_sample(theta, additional_size)
            cumulative_sample.extend(new_elements)
        current_sample = cumulative_sample[:size]
        series_data["samples"][str(size)] = current_sample
        print(f"  n = {size}: {current_sample}")
    all_series.append(series_data)

with open('discrete_uniform_series.json', 'w') as f:
    json.dump({
        'distribution': 'discrete_uniform',
        'parameter': theta,
        'sample_sizes': sample_sizes,
        'num_series': num_series,
        'series': all_series
    }, f, indent=2)

print(f"\nСгенерировано {num_series} серий выборок для дискретного равномерного распределения")
print(f"Параметр θ = {theta}")
print(f"Объемы выборок: {sample_sizes}")
print("Данные сохранены в файл 'discrete_uniform_series.json'")