import json
import numpy as np
from scipy.stats import chi2


def load_samples(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def sturges_k(n):
    return max(2, 1 + int(np.log2(n)))


def estimate_theta_discrete(sample):
    return int(max(sample))


def create_intervals_discrete(k, theta_est):
    base_len = theta_est // k
    remainder = theta_est % k
    intervals = []
    start = 1
    for i in range(k):
        length = base_len + (1 if i < remainder else 0)
        end = start + length - 1
        intervals.append((start, end))
        start = end + 1
    return intervals


def chi2_complex_discrete(sample):
    n = len(sample)

    theta_est = estimate_theta_discrete(sample)

    k = sturges_k(n)

    intervals = create_intervals_discrete(k, theta_est)

    observed = np.zeros(k)
    for value in sample:
        for idx, (low, high) in enumerate(intervals):
            if low <= value <= high:
                observed[idx] += 1
                break

    expected = np.zeros(k)
    for idx, (low, high) in enumerate(intervals):
        length = high - low + 1
        prob = length / theta_est
        expected[idx] = n * prob

    chi2_val = 0
    for obs, exp in zip(observed, expected):
        if exp > 0:
            chi2_val += (obs - exp) ** 2 / exp

    df = k - 2
    critical_value = chi2.ppf(0.95, df)

    return chi2_val, critical_value, k, theta_est, df


def main():
    data = load_samples('discrete_uniform_series.json')
    sample_sizes = data['sample_sizes']
    series = data['series']

    results = []
    theta_estimates = {}

    for size in sample_sizes:
        if size == 5:
            continue

        size_theta_estimates = []
        for series_idx, series_data in enumerate(series):
            sample = series_data['samples'][str(size)]

            chi2_val, critical_value, k, theta_est, df = chi2_complex_discrete(sample)

            conclusion = "Отвергаем" if chi2_val > critical_value else "Принимаем"

            results.append({
                'n': size,
                'Серия': series_idx + 1,
                'k': k,
                'θ_est': theta_est,
                'χ2': round(chi2_val, 2),
                'Критическое': round(critical_value, 2),
                'df': df,
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
    for size, theta_avg in sorted(theta_estimates.items()):
        print(f"{size}\t{theta_avg:.1f}")

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
    for size in sorted(summary.keys()):
        stats = summary[size]
        print(f"{size}\t{stats['Среднее χ2']:10.2f}\t{stats['% отвержений']:10.1f}%")


if __name__ == "__main__":
    main()