import json
import random

def generate_pareto_sample(theta, sample_size):
    sample = []
    for _ in range(sample_size):
        gamma = random.uniform(0, 1)
        mu_gamma = (1 - gamma) ** (-1 / theta)
        sample.append(mu_gamma)

    return sample

theta = float(input("Введите значение параметра θ: "))
sample_size = int(input("Введите объём выборки: "))

sample = generate_pareto_sample(theta, sample_size)

# Сохранение в JSON файл
with open('pareto_sample.json', 'w') as f:
    json.dump({
        'distribution': 'pareto',
        'parameter': theta,
        'sample_size': sample_size,
        'sample': sample
    }, f, indent=2)

print(f"Сгенерирована выборка из {sample_size} значений:")
print(f"Параметр θ = {theta}")
print(f"Выборка: {sample}")
print("Данные сохранены в файл 'pareto_sample.json'")