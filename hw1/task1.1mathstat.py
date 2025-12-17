import json
import math
import random


def generate_discrete_uniform_sample(theta, sample_size):
    sample = []
    for _ in range(sample_size):
        gamma = random.uniform(0, 1)
        mu_gamma = math.floor(gamma * theta) + 1
        sample.append(mu_gamma)
    return sample

theta = int(input("Введите значение параметра θ: "))
sample_size = int(input("Введите объём выборки: "))

sample = generate_discrete_uniform_sample(theta, sample_size)


with open('discrete_uniform_sample.json', 'w') as f:
    json.dump({
        'distribution': 'discrete_uniform',
        'parameter': theta,
        'sample_size': sample_size,
        'sample': sample
    }, f, indent=2)

print(f"Сгенерирована выборка из {sample_size} значений:")
print(f"Параметр θ = {theta}")
print(f"Выборка: {sample}")
print("Данные сохранены в файл 'discrete_uniform_sample.json'")
