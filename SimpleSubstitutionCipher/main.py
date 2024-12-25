import random


from data import coded_texts, none_coded
from SimpleSubstitutionCipherRandomCoder import SimpleSubstitutionCipherRandomCoder
from SimpleSubstitutionCipherCracker import SimpleSubstitutionCipherCracker


import random


def load_unique_words_from_file(file_path):
    unique_words = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip()
            if word:
                unique_words.add(word)
    return unique_words


def get_random_word(word_set):
    return random.choice(list(word_set))


if __name__ == "__main__":
    sscrc = SimpleSubstitutionCipherRandomCoder(language="rus")
    sscc = SimpleSubstitutionCipherCracker(language="rus", text=coded_texts["text1"])

    print(sscc)

    # sscc.decode_whith_frequency()

    # print(f"\n\n{coded_texts["text1"]}\n\n")

    file_path = "zdb-win.txt"
    unique_words = load_unique_words_from_file(file_path)
    random_word = get_random_word(unique_words)
    print("Случайное слово:", random_word)

    print("в" in unique_words)

    # none_coded_text = none_coded["text1"].lower()
    # coded_text = sscrc.code_text(none_coded_text)
    # decoded = sscc.decode_whith_frequency(text=coded_text)

    # print(f"\n\original:\n{none_coded_text}\n\n")
    # print(f"\n\ncoded:\n{coded_text}\n\n")
    # print(f"\n\ndecoded:\n{decoded}\n\n")
