import json
import numpy as np


def estimate_theta_uniform_optimal(sample):
    n = len(sample)
    X_max = np.max(sample)

    if X_max == 1:
        return 1.0

    if n >= 10:
        return ((n + 1) / n) * X_max

    try:
        numerator = X_max ** (n + 1) - (X_max - 1) ** (n + 1)
        denominator = X_max ** n - (X_max - 1) ** n
        result = numerator / denominator
        return result if not np.isnan(result) else ((n + 1) / n) * X_max
    except:
        return ((n + 1) / n) * X_max


def estimate_theta_pareto_optimal(sample):
    n = len(sample)
    if n <= 1:
        return np.nan
    sum_log = np.sum(np.log(sample))
    if sum_log <= 0:
        return np.nan
    return (n - 1) / sum_log


def load_samples(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def compute_optimal_estimates():
    uniform_data = load_samples('discrete_uniform_series.json')
    pareto_data = load_samples('pareto_series.json')

    sample_sizes = uniform_data['sample_sizes']
    num_series = uniform_data['num_series']

    uniform_results = []
    pareto_results = []

    for size in sample_sizes:
        uniform_row = {'n': size}
        pareto_row = {'n': size}

        uniform_estimates = []
        pareto_estimates = []

        for series_idx in range(num_series):
            uniform_sample = uniform_data['series'][series_idx]['samples'][str(size)]
            pareto_sample = pareto_data['series'][series_idx]['samples'][str(size)]

            uniform_est = estimate_theta_uniform_optimal(uniform_sample)
            pareto_est = estimate_theta_pareto_optimal(pareto_sample)

            uniform_estimates.append(uniform_est)
            pareto_estimates.append(pareto_est)

            uniform_row[f'Серия {series_idx + 1}'] = uniform_est
            pareto_row[f'Серия {series_idx + 1}'] = pareto_est

        uniform_row['Среднее'] = np.mean(uniform_estimates)
        pareto_row['Среднее'] = np.mean(pareto_estimates)

        uniform_results.append(uniform_row)
        pareto_results.append(pareto_row)

    return uniform_results, pareto_results


def print_results(uniform_results, pareto_results):
    print("ОПТИМАЛЬНЫЕ ОЦЕНКИ ДЛЯ ДИСКРЕТНОГО РАВНОМЕРНОГО РАСПРЕДЕЛЕНИЯ")
    print("n".ljust(10), end="")
    for i in range(1, 6):
        print(f"Серия {i}".ljust(15), end="")
    print("Среднее".ljust(15))
    print("-" * 95)

    for row in uniform_results:
        print(f"{row['n']}".ljust(10), end="")
        for i in range(1, 6):
            print(f"{row[f'Серия {i}']:.6f}".ljust(15), end="")
        print(f"{row['Среднее']:.6f}".ljust(15))

    print("\n\nОПТИМАЛЬНЫЕ ОЦЕНКИ ДЛЯ РАСПРЕДЕЛЕНИЯ ПАРЕТО")
    print("n".ljust(10), end="")
    for i in range(1, 6):
        print(f"Серия {i}".ljust(15), end="")
    print("Среднее".ljust(15))
    print("-" * 95)

    for row in pareto_results:
        print(f"{row['n']}".ljust(10), end="")
        for i in range(1, 6):
            val = row[f'Серия {i}']
            if np.isnan(val):
                print("не опр.".ljust(15), end="")
            else:
                print(f"{val:.6f}".ljust(15), end="")
        avg_val = row['Среднее']
        if np.isnan(avg_val):
            print("не опр.".ljust(15))
        else:
            print(f"{avg_val:.6f}".ljust(15))


if __name__ == "__main__":
    uniform_results, pareto_results = compute_optimal_estimates()
    print_results(uniform_results, pareto_results)