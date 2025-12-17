import json
import numpy as np
from scipy.stats import chi2


def load_samples(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def sturges_k(n):
    return max(2, 1 + int(np.log2(n)))


def create_intervals(k, theta):
    base_len = theta // k
    remainder = theta % k
    intervals = []
    start = 1
    for i in range(k):
        length = base_len + (1 if i < remainder else 0)
        end = start + length - 1
        intervals.append((start, end))
        start = end + 1
    return intervals


def chi2_statistic(sample, intervals, n, theta):
    observed = [0] * len(intervals)
    for value in sample:
        for idx, (low, high) in enumerate(intervals):
            if low <= value <= high:
                observed[idx] += 1
                break

    expected = []
    for low, high in intervals:
        length = high - low + 1
        prob = length / theta
        expected.append(n * prob)

    chi2_val = 0
    for obs, exp in zip(observed, expected):
        if exp > 0:
            chi2_val += (obs - exp) ** 2 / exp
    return chi2_val


def main():
    data = load_samples('discrete_uniform_series.json')
    theta = data['parameter']
    sample_sizes = data['sample_sizes']
    series = data['series']

    results = []

    for size in sample_sizes:
        if size == 5:
            continue

        k = sturges_k(size)
        intervals = create_intervals(k, theta)
        df = k - 1
        critical_value = chi2.ppf(0.95, df)

        for series_idx, series_data in enumerate(series):
            sample = series_data['samples'][str(size)]
            chi2_val = chi2_statistic(sample, intervals, size, theta)
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
        if size == 5:
            continue
        size_results = [r for r in results if r['n'] == size]
        avg_chi2 = np.mean([r['χ2'] for r in size_results])
        reject_rate = np.mean([1 if r['Вывод'] == 'Отвергаем' else 0 for r in size_results])
        summary[size] = {
            'Среднее χ2': round(avg_chi2, 2),
            '% отвержений': round(reject_rate * 100, 1)
        }

    print("\nСводные результаты:")
    print("n\tСреднее χ2\t% отвержений")
    for size, stats in summary.items():
        print(f"{size}\t{stats['Среднее χ2']:10.2f}\t{stats['% отвержений']:10.1f}%")


if __name__ == "__main__":
    main()