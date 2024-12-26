import random


class SimpleSubstitutionCipherRandomCoder:
    # Предусмотреть языки
    def __init__(self, language):
        languages_letters = {"rus": ["а", "я"], "eng": ["a", "z"]}
        if not language in languages_letters:
            print("Unnown language")
            raise ValueError
        first_letter = languages_letters[language][0]
        last_letter = languages_letters[language][1]
        self.letters = [chr(i) for i in range(ord(first_letter), ord(last_letter) + 1)]
        self.letter_dictionary = {}
        letter_set = set(self.letters)
        for letter in self.letters:
            random_letter = random.choice(list(letter_set))
            letter_set.remove(random_letter)
            self.letter_dictionary[letter] = random_letter

    def code_text(self, text):
        output = []
        for letter in text:
            if letter in self.letter_dictionary:
                output.append(self.letter_dictionary[letter])
            else:
                output.append(letter)

        return "".join(output)
