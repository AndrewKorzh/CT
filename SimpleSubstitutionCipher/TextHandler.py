import re
import math


class TextHandler:
    def __init__(
        self,
        clean_pattern=r"[^a-zA-Zа-яА-ЯёЁ ]",
        lower=True,
    ):
        self.clean_pattern: str = clean_pattern  # r"[^a-zA-Zа-яА-ЯёЁ\s\n]"
        self.lower: bool = lower

    def save_to_file(self, file_name: str, text: str):
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(text)
        except Exception as e:
            print(f"Ошибка при сохранении текста: {e}")

    def read_from_file(self, file_name: str, clean: bool = True):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                content = file.read()

            return self.clean_and_format_text(content)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    def clean_and_format_text(
        self,
        text: str,
    ) -> str:
        if self.lower:
            text = text.lower()
        return re.sub(self.clean_pattern, "", text)

    def get_unigrams(self, text: str) -> dict:
        unigrams = {}
        for char in text:
            if char in unigrams:
                unigrams[char] += 1
            else:
                unigrams[char] = 1
        return unigrams

    def get_bigrams(self, text: str) -> dict:
        bigrams = {}
        for i in range(len(text) - 1):
            bigram = text[i : i + 2]  # Срез возвращает строку.
            bigrams[bigram] = bigrams.get(bigram, 0) + 1
        return bigrams

    # def get_trigrams(self, text: str) -> dict:
    #     trigrams = {}
    #     for i in range(len(text) - 2):
    #         trigram = text[i : i + 3]  # Срез возвращает строку.
    #         trigrams[trigram] = trigrams.get(trigram, 0) + 1
    #     return trigrams

    def get_trigrams(self, text: str) -> dict:
        trigrams = {}
        text = list(text)

        for i in range(len(text) - 2):
            trigram = f"{text[i]}{text[i + 1]}{text[i + 2]}"
            if trigram in trigrams:
                trigrams[trigram] += 1
            else:
                trigrams[trigram] = 1
        return trigrams

    def cosine_similarity(self, vec1: dict, vec2: dict) -> float:
        all_keys = set(vec1.keys()).union(set(vec2.keys()))
        dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in all_keys)
        norm1 = math.sqrt(sum(val**2 for val in vec1.values()))
        norm2 = math.sqrt(sum(val**2 for val in vec2.values()))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def evaluate_unigrams(self, text: str, unigram_stat: dict) -> float:
        unigrams = self.get_unigrams(text)
        return self.cosine_similarity(unigrams, unigram_stat)

    def evaluate_bigrams(self, text: str, bigram_stat: dict) -> float:
        bigrams = self.get_bigrams(text)
        return self.cosine_similarity(bigrams, bigram_stat)

    def evaluate_trigrams(self, text: str, trigram_stat: dict) -> float:
        trigrams = self.get_trigrams(text)
        return self.cosine_similarity(trigrams, trigram_stat)

    def process_file_to_set(self, file_path: str) -> set:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
            cleaned_text = re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s]", "", text)
            word_set = set(cleaned_text.split())
            return word_set
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
            return set()
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")
            return set()

    def calculate_word_match_ratio(
        self, text: str, word_set: set, min_word_length: int = 2
    ) -> float:
        words_in_text = set(
            word for word in text.split() if len(word) >= min_word_length
        )
        matching_words = words_in_text.intersection(word_set)
        if len(words_in_text) == 0:
            return 0.0
        return len(matching_words) / len(words_in_text)


if __name__ == "__main__":
    text_handler = TextHandler()
    open_text = text_handler.read_from_file("./texts/detstvo.txt")
    open_text_unigrams = text_handler.get_unigrams(open_text)
    open_text_bigrams = text_handler.get_bigrams(open_text)
    open_text_trigrams = text_handler.get_trigrams(open_text)

    # text = "Привет! Меня зовут андрей) Как твои дела?"
    text = "Привет. Я даже и не знаю как мне вас благодарить... Не от безысходности своей я прошу помочь мне, но от моего Великого сожаления о содеянном!"
    text = text_handler.read_from_file("./texts/my_text_decoded.txt")
    cleand_text = text_handler.clean_and_format_text(text=text)

    print(cleand_text[:1000])

    print(text_handler.evaluate_unigrams(cleand_text, open_text_unigrams))
    print(text_handler.evaluate_bigrams(cleand_text, open_text_bigrams))
    print(text_handler.evaluate_trigrams(cleand_text, open_text_trigrams))
