import json
import math
import numpy as np

with open('discrete_uniform_series.json', 'r') as f:
    discrete_data = json.load(f)

with open('pareto_series.json', 'r') as f:
    pareto_data = json.load(f)


def estimate_discrete_uniform(sample):

    sample = np.array(sample)
    n = len(sample)
    mean_val = np.mean(sample)
    theta_mm = 2 * mean_val - 1
    theta_mle = np.max(sample)

    return theta_mm, theta_mle


def estimate_pareto(sample):

    sample = np.array(sample)
    n = len(sample)
    mean_val = np.mean(sample)
    if mean_val > 1:
        theta_mm = mean_val / (mean_val - 1)
    else:
        theta_mm = float('inf')

    log_sum = np.sum(np.log(sample))
    if log_sum > 0:
        theta_mle = n / log_sum
    else:
        theta_mle = float('inf')

    return theta_mm, theta_mle


print("=" * 70)
print("ДИСКРЕТНОЕ РАВНОМЕРНОЕ РАСПРЕДЕЛЕНИЕ (θ = 121)")
print("=" * 70)

results_discrete = {}

for series in discrete_data['series']:
    series_num = series['series_number']
    print(f"\nСЕРИЯ {series_num}:")
    print("-" * 40)

    series_results = {}

    for size_str, sample in series['samples'].items():
        size = int(size_str)
        theta_mm, theta_mle = estimate_discrete_uniform(sample)
        theta_mm = float(round(theta_mm, 6))
        theta_mle = float(round(theta_mle, 6))

        series_results[size] = {
            'MM': theta_mm,
            'MLE': theta_mle
        }

        print(f"  n = {size:4d}:  θ_MM = {theta_mm:10.6f},  θ_ММП = {theta_mle:10.6f}")

    results_discrete[series_num] = series_results

print("\n" + "=" * 70)
print("РАСПРЕДЕЛЕНИЕ ПАРЕТО (θ = 12)")
print("=" * 70)

results_pareto = {}

for series in pareto_data['series']:
    series_num = series['series_number']
    print(f"\nСЕРИЯ {series_num}:")
    print("-" * 40)

    series_results = {}

    for size_str, sample in series['samples'].items():
        size = int(size_str)
        theta_mm, theta_mle = estimate_pareto(sample)

        theta_mm = float(round(theta_mm, 6)) if theta_mm != float('inf') else '∞'
        theta_mle = float(round(theta_mle, 6)) if theta_mle != float('inf') else '∞'

        series_results[size] = {
            'MM': theta_mm,
            'MLE': theta_mle
        }

        if theta_mm != '∞' and theta_mle != '∞':
            print(f"  n = {size:4d}:  θ_MM = {theta_mm:10.6f},  θ_ММП = {theta_mle:10.6f}")
        else:
            print(f"  n = {size:4d}:  θ_MM = {theta_mm:>10},  θ_ММП = {theta_mle:>10}")

    results_pareto[series_num] = series_results

all_results = {
    'discrete_uniform': {
        'parameter': discrete_data['parameter'],
        'estimates': results_discrete
    },
    'pareto': {
        'parameter': pareto_data['parameter'],
        'estimates': results_pareto
    }
}

with open('parameter_estimates.json', 'w') as f:
    json.dump(all_results, f, indent=2)

print("\n" + "=" * 70)
print("РЕЗУЛЬТАТЫ СОХРАНЕНЫ")
print("=" * 70)
print("Для каждого распределения, каждой серии и каждого объема выборки")
print("вычислены оценки методом моментов (θ_MM) и методом максимального")
print("правдоподобия (θ_ММП).")
print("\nВсе результаты сохранены в файл 'parameter_estimates.json'")

print("\n" + "=" * 70)
print("СРЕДНИЕ ЗНАЧЕНИЯ ОЦЕНОК ПО 5 СЕРИЯМ")
print("=" * 70)

print("\nДискретное равномерное распределение:")
print("-" * 40)
for size in discrete_data['sample_sizes']:
    mm_vals = []
    mle_vals = []

    for series_num in range(1, 6):
        mm_val = results_discrete[series_num][size]['MM']
        mle_val = results_discrete[series_num][size]['MLE']
        mm_vals.append(mm_val)
        mle_vals.append(mle_val)

    avg_mm = np.mean(mm_vals)
    avg_mle = np.mean(mle_vals)

    print(f"  n = {size:4d}:  θ_MM = {avg_mm:10.6f},  θ_ММП = {avg_mle:10.6f}")

print("\nРаспределение Парето:")
print("-" * 40)
for size in pareto_data['sample_sizes']:
    mm_vals = []
    mle_vals = []

    for series_num in range(1, 6):
        mm_val = results_pareto[series_num][size]['MM']
        mle_val = results_pareto[series_num][size]['MLE']

        if mm_val != '∞' and mle_val != '∞':
            mm_vals.append(mm_val)
            mle_vals.append(mle_val)

    if mm_vals and mle_vals:
        avg_mm = np.mean(mm_vals)
        avg_mle = np.mean(mle_vals)
        print(f"  n = {size:4d}:  θ_MM = {avg_mm:10.6f},  θ_ММП = {avg_mle:10.6f}")
    else:
        print(f"  n = {size:4d}:  оценки не существуют для некоторых серий")