import random


from data import coded_texts, none_coded
from SimpleSubstitutionCipherRandomCoder import SimpleSubstitutionCipherRandomCoder
from SimpleSubstitutionCipherCracker import SimpleSubstitutionCipherCracker

from SimpleSubstitutionCipherCracker2 import SimpleSubstitutionCipherCracker2

from SimpleSubstitutionCipherCracker3 import SimpleSubstitutionCipherCracker3


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
    # sscc = SimpleSubstitutionCipherCracker(
    #     language="rus",
    #     dictionary_path="10000-russian-words.txt",
    #     text=coded_texts["text2"],
    # )

    # sscc.heuristic_function()

    sscc2 = SimpleSubstitutionCipherCracker3(
        language="rus",
        dictionary_path="10000-russian-words.txt",
        text=sscrc.code_text(
            none_coded["text1"]
        ),  # coded_texts["text2"],  # none_coded["text1"]
    )

    print(sscrc.code_text(none_coded["text1"]))

    print(sscc2.text)
    print(sscc2.decode_text())
    sscc2.heuristic_function(decode=False)
    sscc2.heuristic_function(decode=True)

    # print(sscc2.decode_text())
    # sscc2.best_seq_try(swq_amount=10000)

    # print(f"Исходный текст:\n{sscc2.decode_text()}")
    # sscc2.simulated_annealing(
    #     initial_temperature=50000,
    #     cooling_rate=0.999,  # Медленное охлаждение
    #     max_iterations=50000,
    # )
    # print(f"Декодированный текст:\n{sscc2.decode_text()}")

    # sscc.simulated_annealing(
    #     initial_temperature=50000,
    #     cooling_rate=0.9999,  # Медленное охлаждение
    #     max_iterations=500000,
    # )
    # print(f"\n{sscc.text}\n")
    # print(sscc.decode_text())


#
#
#
#
#
#
# while True:
#     ad = input("f")
#     sscc.shuffle_letters_with_limit()
#     print(sscc.decode_text())
# file_path = "zdb-win.txt"
# unique_words = load_unique_words_from_file(file_path)
# random_word = get_random_word(unique_words)
# print("Случайное слово:", random_word)

# print("в" in unique_words)

# sscc.decode_whith_frequency()

# print(f"\n\n{coded_texts["text1"]}\n\n")

# none_coded_text = none_coded["text1"].lower()
# coded_text = sscrc.code_text(none_coded_text)
# decoded = sscc.decode_whith_frequency(text=coded_text)

# print(f"\n\original:\n{none_coded_text}\n\n")
# print(f"\n\ncoded:\n{coded_text}\n\n")
# print(f"\n\ndecoded:\n{decoded}\n\n")
