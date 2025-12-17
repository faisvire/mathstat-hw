import json
import math
import numpy as np
import random


def generate_pareto_sample(theta, sample_size):
    sample = []
    for _ in range(sample_size):
        gamma = random.uniform(0, 1)
        mu_gamma = (1 - gamma) ** (-1 / theta)
        sample.append(mu_gamma)
    return sample


def load_samples(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def estimate_theta(sample):
    n = len(sample)
    sum_log = sum(math.log(x) for x in sample)
    return n / sum_log if sum_log > 0 else 1.0


def kolmogorov_statistic(sample, theta_est):
    n = len(sample)
    sorted_sample = sorted(sample)

    Dn = 0
    for i, x in enumerate(sorted_sample, 1):
        Fn = i / n
        F_theory = 1 - x ** (-theta_est)
        diff = abs(Fn - F_theory)
        if diff > Dn:
            Dn = diff

    S = (6 * n * Dn + 1) / (6 * math.sqrt(n))
    return Dn, S


def main():
    data = load_samples('pareto_series.json')
    sample_sizes = data['sample_sizes']
    series = data['series']

    big_sample = generate_pareto_sample(theta=12, sample_size=10000)
    theta_est = estimate_theta(big_sample)

    results = []

    for size in sample_sizes:
        for series_idx, series_data in enumerate(series):
            sample = series_data['samples'][str(size)]
            Dn, S = kolmogorov_statistic(sample, theta_est)
            conclusion = "Отвергаем" if S > 1.358 else "Принимаем"

            results.append({
                'n': size,
                'Серия': series_idx + 1,
                'Dn': round(Dn, 6),
                'S': round(S, 6),
                'Критическое': 1.358,
                'Вывод': conclusion
            })

    print("n\tСерия\tDn\t\tS\t\tКрит.\tВывод")
    print("-" * 70)
    for res in results:
        print(f"{res['n']}\t{res['Серия']}\t{res['Dn']:.6f}\t{res['S']:.6f}\t{res['Критическое']}\t{res['Вывод']}")

    summary = {}
    for size in sample_sizes:
        size_results = [r for r in results if r['n'] == size]
        avg_Dn = np.mean([r['Dn'] for r in size_results])
        avg_S = np.mean([r['S'] for r in size_results])
        reject_rate = np.mean([1 if r['Вывод'] == 'Отвергаем' else 0 for r in size_results])
        summary[size] = {
            'Среднее Dn': round(avg_Dn, 6),
            'Среднее S': round(avg_S, 6),
            '% отвержений': round(reject_rate * 100, 1)
        }

    print("\nСводные результаты:")
    print("n\tСреднее Dn\tСреднее S\t% отвержений")
    for size in sample_sizes:
        stats = summary[size]
        print(f"{size}\t{stats['Среднее Dn']:.6f}\t{stats['Среднее S']:.6f}\t{stats['% отвержений']:10.1f}%")

    print(f"\nОценка параметра θ по большой выборке: {theta_est:.6f}")


if __name__ == "__main__":
    main()