from char_frequencies import char_frequencies


class SimpleSubstitutionCipherCracker:
    def __init__(self, text: str, language="rus"):
        self.language_char_frequencies = char_frequencies.get(language, None)
        if not self.language_char_frequencies:
            raise ValueError
        self.text = text.lower()
        self.letters_coded_text = None
        self.letters_decoded_text = None
        self.decoded_letters_start_indexes = None
        self.setup()

    def __str__(self):
        out = [
            f"Порядок букв согласно частотам текста:\n{self.letters_coded_text}",
            f"Порядок букв согласно частотам языка:\n{self.letters_decoded_text}",
            f"Порядок букв согласно частотам языка:\n{self.decoded_letters_start_indexes}",
        ]
        return "\n".join(out)

    # Надо как-то поприятней разделить, сделать что-то типа reset
    def setup(self):
        frequency_dict = {}
        self.text = self.text.lower()
        for letter in self.text:
            if letter.isalpha():
                if letter in frequency_dict:
                    frequency_dict[letter] += 1
                else:
                    frequency_dict[letter] = 1

        sorted_frequency_dict = dict(
            sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)
        )

        self.letters_coded_text = sorted_frequency_dict.keys()

        sorted_language_char_frequencies = dict(
            sorted(
                self.language_char_frequencies.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

        self.letters_decoded_text = sorted_language_char_frequencies.keys()

        self.decoded_letters_start_indexes = {
            letter: i for i, letter in enumerate(self.letters_decoded_text)
        }

    def get_text_frequency_dict(self) -> dict:
        frequency_dict = {}
        self.text = self.text.lower()
        for letter in self.text:
            if letter.isalpha():
                if letter in frequency_dict:
                    frequency_dict[letter] += 1
                else:
                    frequency_dict[letter] = 1
        return frequency_dict

    # Предусмотреть когда в тексте не все буквы
    def merge_dict_by_value(self, dict1: dict, dict2: dict) -> dict:
        sorted_dict1 = dict(
            sorted(dict1.items(), key=lambda item: item[1], reverse=True)
        )
        sorted_dict2 = dict(
            sorted(dict2.items(), key=lambda item: item[1], reverse=True)
        )
        merged_dict = {
            value1: value2
            for (value1, _), (value2, _) in zip(
                sorted_dict1.items(), sorted_dict2.items()
            )
        }

        print(f"\n\n{sorted_dict1}\n\n")
        print(f"\n\n{sorted_dict2}\n\n")
        print(f"\n\n{merged_dict}\n\n")
        return merged_dict

    def decode_whith_frequency(self):
        self.text = self.text.lower()
        text_dictionary = self.get_text_frequency_dict()
        murged_dict = self.merge_dict_by_value(
            text_dictionary, self.language_char_frequencies
        )
        output = []
        for letter in self.text:
            if letter in murged_dict:
                output.append(murged_dict[letter])
            else:
                output.append(letter)
        print("".join(output))
        return "".join(output)
