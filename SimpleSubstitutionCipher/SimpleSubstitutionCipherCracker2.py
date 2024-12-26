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


def clean_and_format_text(text: str):
    return re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s\n]", "", text.lower())


class SimpleSubstitutionCipherCracker2:
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
        print(words)

        valid_letters_count = 0
        for word in words:
            if word in self.all_words_set:
                valid_letters_count += len(word)

        print(
            f"Valid letters in words: {valid_letters_count}/{self.letter_in_text_amount}"
        )
        return valid_letters_count

    def generate_neighbor(self, max_distance=2):
        n = len(self.letters_decoded_text)
        i = random.randint(0, n - 1)
        start = max(0, i - max_distance)
        end = min(n - 1, i + max_distance)
        j = random.choice([k for k in range(start, end + 1) if k != i])
        return i, j

    def swap_decoded_letters(self, i, j):
        self.letters_decoded_text[i], self.letters_decoded_text[j] = (
            self.letters_decoded_text[j],
            self.letters_decoded_text[i],
        )

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

    def shuffle_letters_with_limit(self, max_distance=3):
        n = len(self.letters_decoded_text)
        shuffled = self.letters_decoded_text.copy()
        for i in range(n):
            start = max(0, i - max_distance)
            end = min(n - 1, i + max_distance)
            j = random.randint(start, end)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        self.letters_decoded_text = shuffled

    def __str__(self):
        return "\n".join(
            [
                f"Text frequency order: {self.letters_coded_text}",
                f"Language frequency order: {self.letters_decoded_text}",
                f"Frequency dictionary: {self.text_f_dict}",
            ]
        )
