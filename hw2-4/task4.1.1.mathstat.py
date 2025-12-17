import json
import numpy as np


def load_pareto_samples():
    with open('pareto_series.json', 'r') as f:
        data = json.load(f)
    return data


def kolmogorov_statistic(sample, theta=12):
    n = len(sample)

    def pareto_cdf(x):
        return 1 - x ** (-theta)

    x_sorted = np.sort(sample)
    i = np.arange(1, n + 1)
    F_n = i / n
    F = pareto_cdf(x_sorted)

    D_plus = np.max(np.abs(F_n - F))
    D_minus = np.max(np.abs(F - (i - 1) / n))
    D_n = max(D_plus, D_minus)

    return D_n


def perform_kolmogorov_tests():
    data = load_pareto_samples()
    sample_sizes = data['sample_sizes']
    num_series = data['num_series']
    theta_true = data['parameter']

    results = []

    print("КРИТЕРИЙ КОЛМОГОРОВА ДЛЯ РАСПРЕДЕЛЕНИЯ ПАРЕТО")
    print(f"θ={theta_true}, α=0.05, крит.знач.=1.358")
    print("=" * 80)

    for size in sample_sizes:
        for series_idx in range(num_series):
            sample = data['series'][series_idx]['samples'][str(size)]

            D_n = kolmogorov_statistic(sample, theta_true)
            S = (6 * size * D_n + 1) / (6 * np.sqrt(size))
            reject = S > 1.358

            results.append({
                'n': size,
                'Серия': series_idx + 1,
                'D_n': D_n,
                'S': S,
                'Отклоняем': reject
            })

    for size in sample_sizes:
        print(f"\nn = {size}:")
        print(f"{'Серия':<8} {'D_n':<12} {'S':<12} {'Вывод':<15}")
        print("-" * 50)

        for result in results:
            if result['n'] == size:
                status = "ОТКЛОНЯЕМ" if result['Отклоняем'] else "ПРИНИМАЕМ"
                print(f"{result['Серия']:<8} {result['D_n']:<12.6f} {result['S']:<12.6f} {status:<15}")

    print("\n" + "=" * 80)
    print("СРЕДНИЕ ЗНАЧЕНИЯ ПО РАЗМЕРАМ ВЫБОРОК:")
    print(f"{'n':<8} {'Средн. D_n':<15} {'Средн. S':<15} {'% откл.':<10}")
    print("-" * 80)

    for size in sample_sizes:
        size_results = [r for r in results if r['n'] == size]
        avg_D = np.mean([r['D_n'] for r in size_results])
        avg_S = np.mean([r['S'] for r in size_results])
        reject_rate = np.mean([r['Отклоняем'] for r in size_results]) * 100
        print(f"{size:<8} {avg_D:<15.6f} {avg_S:<15.6f} {reject_rate:<10.1f}%")


if __name__ == "__main__":
    perform_kolmogorov_tests()