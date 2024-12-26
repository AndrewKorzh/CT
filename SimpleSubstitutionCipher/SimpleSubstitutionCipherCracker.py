import random
import math
import re

from char_frequencies import char_frequencies


def load_unique_words_from_file(file_path):
    unique_words = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip()
            if word:
                unique_words.add(word)
    return unique_words


class SimpleSubstitutionCipherCracker:
    def __init__(
        self,
        text: str,
        dictionary_path: str,
        language="rus",
    ):
        self.language_char_frequencies = None
        self.text = None
        self.letters_coded_text = None
        self.letters_decoded_text = None
        self.decoded_letters_start_indexes = None
        self.all_words_set = None
        self.alphabet_length = None
        self.text_f_dict = None
        self.letter_in_text_amount = None
        self.reset(
            text=text,
            dictionary_path=dictionary_path,
            language=language,
        )

    def reset(
        self,
        language: str,
        dictionary_path: str,
        text: str,
    ):
        self.language_char_frequencies = char_frequencies.get(language, None)
        if not self.language_char_frequencies:
            print("Unknown language")
            raise ValueError

        self.all_words_set = load_unique_words_from_file(file_path=dictionary_path)

        self.letter_in_text_amount = 0
        frequency_dict = {}
        self.text = text.lower()
        for letter in self.text:
            if letter.isalpha():
                self.letter_in_text_amount += 1
                if letter in frequency_dict:
                    frequency_dict[letter] += 1
                else:
                    frequency_dict[letter] = 1

        sorted_frequency_dict = dict(
            sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)
        )

        self.text_f_dict = sorted_frequency_dict
        self.letters_coded_text = list(sorted_frequency_dict.keys())

        sorted_language_char_frequencies = dict(
            sorted(
                self.language_char_frequencies.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

        self.letters_decoded_text = list(sorted_language_char_frequencies.keys())

        self.decoded_letters_start_indexes = {
            letter: i for i, letter in enumerate(self.letters_decoded_text)
        }
        self.alphabet_length = len(self.letters_decoded_text)

    # Тут смотрим насколько далеко ушли по индексам от ожидаемого и смотрим на наличие слов
    def heuristic_function(self):
        decoded_text = self.text  # self.decode_text()
        words = re.findall(r"[a-zA-Zа-яА-ЯёЁ]+", decoded_text)

        score = 0
        letters_on_right_place_count = 0
        for word in words:
            if word in self.all_words_set:
                letters_on_right_place_count += len(word)
                score += len(word) ** 2

        print(f"Всего букв: {self.letter_in_text_amount}")
        print(f"Количество букв в осммысленных словах: {letters_on_right_place_count}")

        return score

    def generate_neighbor(self, max_distance=2):
        n = len(self.letters_decoded_text)
        # Выбираем случайный индекс i
        i = random.randint(0, n - 1)

        # Определяем допустимые индексы для j в пределах max_distance
        start = max(0, i - max_distance)
        end = min(n - 1, i + max_distance)

        # Выбираем случайный индекс j в пределах [start, end], исключая i
        j = random.choice([k for k in range(start, end + 1) if k != i])

        return i, j

    def swap_decoded_leters(self, i, j):
        l1 = self.letters_decoded_text[i]
        self.letters_decoded_text[i] = self.letters_decoded_text[j]
        self.letters_decoded_text[j] = l1
        return

    def simulated_annealing(self, initial_temperature, cooling_rate, max_iterations):
        current_score = self.heuristic_function()
        temperature = initial_temperature

        for _ in range(max_iterations):
            i, j = self.generate_neighbor()
            self.swap_decoded_leters(i, j)
            neighbor_score = self.heuristic_function()

            if neighbor_score > current_score:
                current_score = neighbor_score
            else:
                acceptance_probability = math.exp(
                    (neighbor_score - current_score) / temperature
                )
                self.swap_decoded_leters(i, j)
                if random.random() < acceptance_probability:
                    self.swap_decoded_leters(i, j)
                    current_score = neighbor_score
            temperature *= cooling_rate
            if temperature < 1e-6:
                break

        return True

    def shuffle_letters_with_limit(self, max_distance=3):
        n = len(self.letters_decoded_text)
        shuffled = self.letters_decoded_text.copy()
        for i in range(n):
            # Определяем границы для перемещения элемента
            start = max(0, i - max_distance)
            end = min(n - 1, i + max_distance)

            # Выбираем случайный индекс в пределах допустимого диапазона
            j = random.randint(start, end)

            # Меняем местами элементы
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]

        self.letters_decoded_text = shuffled

    def __str__(self):
        out = [
            f"Порядок букв согласно частотам текста:\n{self.letters_coded_text}",
            f"Порядок букв согласно частотам языка:\n{self.letters_decoded_text}",
            f"Порядок букв согласно частотам языка:\n{self.decoded_letters_start_indexes}",
            f"{self.text_f_dict}",
        ]
        return "\n".join(out)

    def decode_text(self):
        decode_map = dict(zip(self.letters_coded_text, self.letters_decoded_text))
        output = []
        for letter in self.text:
            if letter in decode_map:
                output.append(decode_map[letter])
            else:
                output.append(letter)
        return "".join(output)

        #         # for letter in word:
        #         #     if letter in self.language_char_frequencies:
        #         #         score += self.language_char_frequencies[
        #         #             letter
        #         #         ]  # Вес по частоте буквы

        # print(f"heu {score}")
        # # Оценка позиций букв в алфавите
        # for i in range(self.alphabet_length):
        #     letter = self.letters_decoded_text[i]
        #     score += (
        #         1
        #         - (
        #             abs(self.decoded_letters_start_indexes[letter] - i)
        #             / self.alphabet_length
        #         )
        #     ) * 10

        # print(f"heuristic_function: {score}")
