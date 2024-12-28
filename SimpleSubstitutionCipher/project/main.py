from TextHandler import TextHandler

if __name__ == "__main__":
    th = TextHandler()
    word_set = th.process_file_to_set(
        file_path="./dictionaries/10000-russian-words.txt"
    )

    print(
        th.calculate_word_match_ratio(
            "привет дорогой друг как твои дела ы в ы", word_set
        )
    )
