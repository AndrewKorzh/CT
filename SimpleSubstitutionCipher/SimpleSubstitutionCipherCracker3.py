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


import re


def gradual_permutation(sequence, steps):
    n = len(sequence)
    current_sequence = sequence[:]
    seen = {tuple(current_sequence)}  # Хранение уникальных последовательностей

    for _ in range(steps):
        for _ in range(n * 2):  # Попытки найти уникальную перестановку
            # Выбираем два соседних индекса для минимального изменения
            i = random.randint(0, n - 2)
            j = i + 1

            # Создаем новую последовательность с обменом мест
            new_sequence = current_sequence[:]
            new_sequence[i], new_sequence[j] = new_sequence[j], new_sequence[i]

            # Если перестановка уникальна, запоминаем и возвращаем её
            if tuple(new_sequence) not in seen:
                seen.add(tuple(new_sequence))
                current_sequence = new_sequence
                yield current_sequence
                break
        else:
            # Если не удалось найти уникальную перестановку
            raise RuntimeError("Не удалось сгенерировать уникальную последовательность")


def seq_entropy_rate(start_seq, current_seq):
    score = 0
    for i in range(len(start_seq)):
        delta = abs(current_seq.index(start_seq[i]) - i)
        score += delta
    return score


def clean_and_format_text(text: str):
    return re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s\n]", "", text.lower())


class SimpleSubstitutionCipherCracker3:
    def __init__(self, text: str, dictionary_path: str, language="rus"):
        self.language_char_frequencies = None
        self.text = None
        self.letters_coded_text = None
        self.letters_decoded_text = None
        self.decoded_letters_start_indexes = None
        self.all_words_set = None
        self.alphabet_length = None
        self.text_f_dict = None
        self.letter_in_text_amount = None
        self.decoded_text = None
        self.reset(text=text, dictionary_path=dictionary_path, language=language)

    def reset(self, language: str, dictionary_path: str, text: str):
        self.language_char_frequencies = char_frequencies.get(language, None)
        if not self.language_char_frequencies:
            raise ValueError("Unknown language")

        self.all_words_set = load_unique_words_from_file(file_path=dictionary_path)

        self.letter_in_text_amount = 0
        frequency_dict = {}
        self.text = clean_and_format_text(text=text)
        for letter in self.text:
            if letter.isalpha():
                self.letter_in_text_amount += 1
                frequency_dict[letter] = frequency_dict.get(letter, 0) + 1

        self.text_f_dict = dict(
            sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)
        )

        self.letters_coded_text = list(self.text_f_dict.keys())

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

    def heuristic_function(self, decode=True):
        if decode:
            decoded_text = self.decode_text()
        else:
            decoded_text = self.text
        words = re.findall(r"[a-zA-Zа-яА-ЯёЁ]+", decoded_text)
        # print(words)

        valid_letters_count = 0
        # Не пойдёт, шума много как-то, надо еще добавлять
        for word in words:
            if word in self.all_words_set:
                print(f"{word}", end=" ")
                valid_letters_count += len(word)
        print()

        print(
            f"Valid letters in words: {valid_letters_count}/{self.letter_in_text_amount}"
        )
        return valid_letters_count

    # Можно попробовать, если приносит результат, то сделать её - эту последовательность отправной
    def best_seq_try(self, swq_amount):
        sequence = self.letters_decoded_text[:]
        best_seq = self.letters_decoded_text[:]
        best_h = self.heuristic_function()
        steps = swq_amount
        for idx, seq in enumerate(gradual_permutation(sequence, steps)):
            self.letters_decoded_text = seq
            h = self.heuristic_function()
            if h > best_h:
                best_seq = seq
                best_h = h
            print(
                f"Шаг {idx + 1}: {''.join(seq)} - {seq_entropy_rate(start_seq=sequence, current_seq=seq)} h: {h}"
            )
        print(f"best_h: {best_h}")
        self.letters_decoded_text = best_seq
        return

    def best_seq_try2(self, swq_amount):
        sequence = self.letters_decoded_text[:]  # Исходная последовательность
        best_seq = self.letters_decoded_text[:]  # Изначально лучшая последовательность
        best_h = self.heuristic_function()  # Изначальное значение функции
        steps = swq_amount  # Количество шагов

        for idx, seq in enumerate(gradual_permutation(sequence, steps)):
            self.letters_decoded_text = seq
            h = self.heuristic_function()  # Оценка новой последовательности

            # Если нашли улучшение
            if h > best_h:
                best_seq = seq  # Обновляем лучшую последовательность
                best_h = h  # Обновляем значение функции
                sequence = (
                    seq  # Обновляем последовательность, с которой будем продолжать
                )
                steps = swq_amount  # Восстанавливаем количество шагов для дальнейшего перебора

            # Если нет улучшения, продолжаем перебор
            else:
                # Для продолжения, если нужно
                pass

            # (необязательно) можно добавить вывод для отслеживания шагов
            # print(f"Шаг {idx + 1}: {''.join(seq)} - h: {h}")

        print(f"best_h: {best_h}")
        return best_seq  # Возвращаем лучшую последовательность

    def simulated_annealing(self, initial_temperature, cooling_rate, max_iterations):
        current_score = self.heuristic_function()
        temperature = initial_temperature

        for _ in range(max_iterations):
            i, j = self.generate_neighbor()
            self.swap_decoded_letters(i, j)
            neighbor_score = self.heuristic_function()

            if neighbor_score > current_score:
                current_score = neighbor_score
            else:
                acceptance_probability = math.exp(
                    (neighbor_score - current_score) / temperature
                )
                if random.random() < acceptance_probability:
                    current_score = neighbor_score
                else:
                    self.swap_decoded_letters(i, j)  # Undo swap

            temperature *= cooling_rate
            if temperature < 1e-6:
                break

        return current_score

    def decode_text(self):
        decode_map = dict(zip(self.letters_coded_text, self.letters_decoded_text))
        return "".join(decode_map.get(char, char) for char in self.text)

    def __str__(self):
        return "\n".join(
            [
                f"Text frequency order: {self.letters_coded_text}",
                f"Language frequency order: {self.letters_decoded_text}",
                f"Frequency dictionary: {self.text_f_dict}",
            ]
        )
