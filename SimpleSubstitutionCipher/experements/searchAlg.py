import random
import math


# Пример эвристической функции (например, соответствие частотам)
# Эта функция должна быть адаптирована под конкретную задачу
def heuristic_function(arrangement):
    # Примерная эвристика: чем ближе порядок букв к частотности, тем лучше
    frequency_order = ["a", "б", "в", "г", "д", "е"]
    score = 0
    for i, char in enumerate(arrangement):
        if i < len(frequency_order) and char == frequency_order[i]:
            score += 1  # Чем больше букв на правильных местах, тем выше оценка
    return score


# Функция для генерирования соседней перестановки (перестановка двух букв)
def generate_neighbor(arrangement):
    neighbor = arrangement[:]
    i, j = random.sample(range(len(arrangement)), 2)  # Выбираем два случайных индекса
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]  # Меняем местами буквы
    return neighbor


# Симуляционное отжигание
def simulated_annealing(
    initial_arrangement, initial_temperature, cooling_rate, max_iterations
):
    current_arrangement = initial_arrangement
    current_score = heuristic_function(current_arrangement)

    temperature = initial_temperature

    for _ in range(max_iterations):
        # Генерируем соседнюю перестановку
        neighbor = generate_neighbor(current_arrangement)
        neighbor_score = heuristic_function(neighbor)

        # Если соседнее решение лучше, принимаем его
        if neighbor_score > current_score:
            current_arrangement = neighbor
            current_score = neighbor_score
        else:
            # Если не лучше, принимаем с вероятностью, зависящей от температуры
            acceptance_probability = math.exp(
                (neighbor_score - current_score) / temperature
            )
            if random.random() < acceptance_probability:
                current_arrangement = neighbor
                current_score = neighbor_score

        # Понижаем температуру
        temperature *= cooling_rate

        # Если температура очень низкая, заканчиваем
        if temperature < 1e-6:
            break

    return current_arrangement


# Пример начальных данных
initial_arrangement = ["a", "в", "д", "е", "г", "б"]
initial_temperature = 100  # Начальная температура
cooling_rate = 0.995  # Коэффициент охлаждения
max_iterations = 1000  # Максимальное количество итераций

# Запуск симуляционного отжига
final_arrangement = simulated_annealing(
    initial_arrangement, initial_temperature, cooling_rate, max_iterations
)

# Результат
print("Финальная перестановка:", final_arrangement)
