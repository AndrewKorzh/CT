import random

from TextHandler import TextHandler


class CipherCracker(TextHandler):
    def __init__(
        self,
        clean_pattern=r"[^a-zA-Zа-яА-ЯёЁ ]",
        lower=True,
    ):
        super().__init__(clean_pattern, lower)

    def unigrams_to_mapping(self, uni1: dict, uni2: dict) -> dict:
        sorted_uni1 = sorted(uni1.items(), key=lambda item: item[1], reverse=True)
        sorted_uni2 = sorted(uni2.items(), key=lambda item: item[1], reverse=True)
        if len(sorted_uni2) < len(sorted_uni1):
            raise ValueError(
                "В uni2 недостаточно уникальных символов для создания отображения"
            )
        mapping = {}
        for (char1, _), (char2, _) in zip(sorted_uni1, sorted_uni2):
            mapping[char1] = char2

        return mapping

    def apply_mapping(self, text: str, mapping: dict) -> str:
        translated_text = []
        for char in text:
            if char in mapping:
                translated_text.append(mapping[char])
            else:
                translated_text.append(char)

        return "".join(translated_text)

    def random_letter_mapping_swap(self, letter_mapping: dict, max_distance: int = 3):
        keys = list(letter_mapping.keys())
        index1 = random.randint(0, len(keys) - 1)
        index2 = random.randint(
            max(0, index1 - max_distance), min(len(keys) - 1, index1 + max_distance)
        )
        key1 = keys[index1]
        key2 = keys[index2]
        letter_mapping[key1], letter_mapping[key2] = (
            letter_mapping[key2],
            letter_mapping[key1],
        )
        return key1, key2

    # Текст1, текст2, функция для оценки, eps - для выхода, максимально число итераций
    def simple_chrack(
        self,
        open_text: str,
        coded_text: str,
        score_function_name="evaluate_trigrams",
        max_best_score_iters=500,
        max_iters=1000,
        max_distance_swap=3,
        word_set=None,
        word_impact_factor=0.5,
        min_word_length=3,
    ):
        # Сделать нормальное переключение
        open_text_unigrams = self.get_unigrams(open_text)
        open_text_bigrams = self.get_bigrams(open_text)
        open_text_trigrams = self.get_trigrams(open_text)

        if score_function_name == "evaluate_unigrams":
            score_function = self.evaluate_unigrams
            unigrams = open_text_unigrams
        elif score_function_name == "evaluate_bigrams":
            score_function = self.evaluate_bigrams
            unigrams = open_text_bigrams
        elif score_function_name == "evaluate_trigrams":
            score_function = self.evaluate_trigrams
            unigrams = open_text_trigrams
        else:
            raise ValueError("Wrong score_function_name")

        coded_text_unigrams = self.get_unigrams(coded_text)
        letter_mapping = self.unigrams_to_mapping(
            coded_text_unigrams, open_text_unigrams
        )

        text = self.apply_mapping(coded_text, letter_mapping)

        start_score = score_function(text, unigrams)
        score = start_score
        if word_set:
            score += (
                self.calculate_word_match_ratio(text, word_set, min_word_length)
                * word_impact_factor
            )
        best_score = start_score
        max_best_score_iters_count = 0
        for i in range(max_iters):
            key1, key2 = self.random_letter_mapping_swap(
                letter_mapping, max_distance=max_distance_swap
            )
            text = self.apply_mapping(coded_text, letter_mapping)
            score = score_function(text, unigrams)
            if word_set:
                score += (
                    self.calculate_word_match_ratio(text, word_set, min_word_length)
                    * word_impact_factor
                )
            print(f"{i}) {"".join(list(letter_mapping.values()))} - {score}")
            if score > best_score:
                best_score = score
                max_best_score_iters_count = 0

            else:
                max_best_score_iters_count += 1
                l = letter_mapping[key1]
                letter_mapping[key1] = letter_mapping[key2]
                letter_mapping[key2] = l
            if max_best_score_iters_count > max_best_score_iters:
                break

        print(f"start_score - {start_score}, best_score - {best_score}")

        return letter_mapping  # self.apply_mapping(coded_text, letter_mapping),


if __name__ == "__main__":
    cipher_cracker = CipherCracker()
    open_text = cipher_cracker.read_from_file("./texts/detstvo.txt")

    # text = "Привет дорогой друг! Я тебя приветствую! Бу, испугался? Не бойся, я друг, я тебя не обижу! Иди сюда, иди ко мне!"
    text = cipher_cracker.read_from_file("./texts/text2.txt")

    cleand_text = cipher_cracker.clean_and_format_text(text)

    word_set = cipher_cracker.process_file_to_set(
        file_path="./dictionaries/10000-russian-words.txt"
    )

    decoded_text = cipher_cracker.simple_chrack(
        open_text=open_text,
        coded_text=cleand_text,
        max_iters=10000,
        max_best_score_iters=500,
        max_distance_swap=3,
        score_function_name="evaluate_bigrams",
        word_set=word_set,
        word_impact_factor=0.5,
        min_word_length=4,
    )

    print(decoded_text)
