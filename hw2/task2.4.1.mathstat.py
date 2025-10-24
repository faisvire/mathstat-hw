import json

with open('discrete_uniform_series.json', 'r') as f:
    data = json.load(f)

sample_sizes = data['sample_sizes']
series = data['series']

for size in sample_sizes:
    print(f"\nОбъем выборки n = {size}:")

    x_bars = []  # выборочные средние
    s_squares = []  # выборочные дисперсии

    for i, series_data in enumerate(series, 1):
        sample = series_data['samples'][str(size)]
        n = len(sample)
        x_bar = sum(sample) / n
        squared_deviations = sum((x - x_bar) ** 2 for x in sample)
        s_squared = squared_deviations / n
        x_bars.append(x_bar)
        s_squares.append(s_squared)
        print(f"  Серия {i}: X̄ = {x_bar:.6f}, S̄² = {s_squared:.6f}")

    avg_x_bar = sum(x_bars) / len(x_bars)
    avg_s_squared = sum(s_squares) / len(s_squares)
    print(f"  Среднее: X̄ = {avg_x_bar:.6f}, S̄² = {avg_s_squared:.6f}")