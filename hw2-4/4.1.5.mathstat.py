import json
import math
import numpy as np
from scipy.stats import chi2


def load_samples(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def sturges_k(n):
    return max(2, 1 + int(np.log2(n)))


def pareto_cdf(x, theta):
    return 1 - x ** (-theta)


def create_intervals_pareto(sample, k, theta):
    sorted_sample = sorted(sample)
    min_val = 1.0
    max_val = sorted_sample[-1] * 1.01

    probs = np.linspace(0, 1, k + 1)[1:-1]
    boundaries = [min_val]
    for p in probs:
        boundary = (1 - p) ** (-1 / theta)
        boundaries.append(boundary)
    boundaries.append(max_val)

    return boundaries


def chi2_complex_pareto(sample):
    n = len(sample)

    theta_est = n / sum(math.log(x) for x in sample)

    k = sturges_k(n)

    boundaries = create_intervals_pareto(sample, k, theta_est)

    observed = np.zeros(k)
    for value in sample:
        for i in range(k):
            if boundaries[i] <= value < boundaries[i + 1]:
                observed[i] += 1
                break
        if value >= boundaries[-1]:
            observed[-1] += 1

    expected = np.zeros(k)
    for i in range(k):
        prob = pareto_cdf(boundaries[i + 1], theta_est) - pareto_cdf(boundaries[i], theta_est)
        expected[i] = n * prob

    chi2_val = 0
    for obs, exp in zip(observed, expected):
        if exp > 0:
            chi2_val += (obs - exp) ** 2 / exp

    df = k - 2
    critical_value = chi2.ppf(0.95, df)

    return chi2_val, critical_value, k, theta_est


def main():
    data = load_samples('pareto_series.json')
    sample_sizes = data['sample_sizes']
    series = data['series']

    results = []
    theta_estimates = {}

    for size in sample_sizes:
        size_theta_estimates = []
        for series_idx, series_data in enumerate(series):
            sample = series_data['samples'][str(size)]

            chi2_val, critical_value, k, theta_est = chi2_complex_pareto(sample)

            conclusion = "Отвергаем" if chi2_val > critical_value else "Принимаем"

            results.append({
                'n': size,
                'Серия': series_idx + 1,
                'k': k,
                'θ_est': round(theta_est, 4),
                'χ2': round(chi2_val, 2),
                'Критическое': round(critical_value, 2),
                'df': k - 2,
                'Вывод': conclusion
            })

            size_theta_estimates.append(theta_est)

        theta_estimates[size] = np.mean(size_theta_estimates)

    print("n\tСерия\tk\tθ_est\tχ2\t\tКрит.зн.\tdf\tВывод")
    print("-" * 80)
    for res in results:
        print(
            f"{res['n']}\t{res['Серия']}\t{res['k']}\t{res['θ_est']}\t{res['χ2']:8.2f}\t{res['Критическое']:8.2f}\t{res['df']}\t{res['Вывод']}")

    print("\nСредние оценки θ по объему выборки:")
    print("n\tСреднее θ")
    for size, theta_avg in theta_estimates.items():
        print(f"{size}\t{theta_avg:.4f}")

    summary = {}
    for size in sample_sizes:
        size_results = [r for r in results if r['n'] == size]
        avg_chi2 = np.mean([r['χ2'] for r in size_results])
        reject_rate = np.mean([1 if r['Вывод'] == 'Отвергаем' else 0 for r in size_results])
        summary[size] = {
            'Среднее χ2': round(avg_chi2, 2),
            '% отвержений': round(reject_rate * 100, 1)
        }

    print("\nСводные результаты:")
    print("n\tСреднее χ2\t% отвержений")
    for size in sample_sizes:
        stats = summary[size]
        print(f"{size}\t{stats['Среднее χ2']:10.2f}\t{stats['% отвержений']:10.1f}%")


if __name__ == "__main__":
    main()