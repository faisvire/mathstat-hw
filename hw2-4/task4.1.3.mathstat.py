import json
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


def chi2_statistic_pareto(sample, boundaries, theta):
    k = len(boundaries) - 1
    observed = np.zeros(k)

    for value in sample:
        for i in range(k):
            if boundaries[i] <= value < boundaries[i + 1]:
                observed[i] += 1
                break
        if value >= boundaries[-1]:
            observed[-1] += 1

    n = len(sample)
    expected = np.zeros(k)
    for i in range(k):
        prob = pareto_cdf(boundaries[i + 1], theta) - pareto_cdf(boundaries[i], theta)
        expected[i] = n * prob

    chi2_val = 0
    for obs, exp in zip(observed, expected):
        if exp > 0:
            chi2_val += (obs - exp) ** 2 / exp
    return chi2_val


def main():
    data = load_samples('pareto_series.json')
    theta = data['parameter']
    sample_sizes = data['sample_sizes']
    series = data['series']

    results = []

    for size in sample_sizes:
        k = sturges_k(size)
        df = k - 1
        critical_value = chi2.ppf(0.95, df)

        for series_idx, series_data in enumerate(series):
            sample = series_data['samples'][str(size)]
            boundaries = create_intervals_pareto(sample, k, theta)
            chi2_val = chi2_statistic_pareto(sample, boundaries, theta)
            conclusion = "Отвергаем" if chi2_val > critical_value else "Принимаем"

            results.append({
                'n': size,
                'Серия': series_idx + 1,
                'k_интервалов': k,
                'χ2': round(chi2_val, 2),
                'Критическое': round(critical_value, 2),
                'Вывод': conclusion
            })

    print("n\tСерия\tk\tχ2\t\tКрит.зн.\tВывод")
    print("-" * 60)
    for res in results:
        print(
            f"{res['n']}\t{res['Серия']}\t{res['k_интервалов']}\t{res['χ2']:8.2f}\t{res['Критическое']:8.2f}\t{res['Вывод']}")

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