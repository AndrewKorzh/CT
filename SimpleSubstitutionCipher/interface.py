import math
import tkinter as tk
from tkinter import filedialog

from CipherCracker import CipherCracker


DEFAULT_PADX = 5
DEFAULT_PADY = 2
TEXT_WIDTH = 80

TEXT_HEIGHT = 30


class CipherCrackerInterface:
    def __init__(self, master, cipher_cracker: CipherCracker):
        self.master = master
        self.master.title("Cipher Cracker")
        # self.master.geometry("800x600")
        self.cipher_cracker = cipher_cracker

        self.open_text = None

        self.word_set = None
        self.coded_text = ""
        self.decoded_text = ""

        self.mapping_width = 800  # Ширина области отображения

        self.row = 0

        self.init_ui()

    def init_ui(self):
        self.open_text_label = tk.Label(self.master, text="Открытый текст:")
        self.open_text_label.grid(
            row=self.row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.open_text_entry = tk.Entry(
            self.master,
            width=math.floor(TEXT_WIDTH * 1.2),
        )
        self.open_text_entry.grid(
            row=self.row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, columnspan=9
        )
        self.load_button = tk.Button(
            self.master, text="Загрузить", command=self.load_open_text
        )
        self.load_button.grid(
            row=self.row, column=10, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.row += 1

        # Словарь
        self.dictionary_label = tk.Label(self.master, text="Словарь (не обязательно):")
        self.dictionary_label.grid(
            row=self.row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.dictionary_entry = tk.Entry(
            self.master, width=math.floor(TEXT_WIDTH * 1.2)
        )
        self.dictionary_entry.grid(
            row=self.row,
            column=0,
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
            columnspan=9,
        )
        self.load_dict_button = tk.Button(
            self.master, text="Загрузить", command=self.load_dictionary
        )
        self.load_dict_button.grid(
            row=self.row, column=10, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )

        self.row += 1

        # Окно для закодированного текста
        self.coded_text_label = tk.Label(self.master, text="Закодированный текст:")
        self.coded_text_label.grid(
            row=self.row,
            column=0,
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
            sticky="w",
            columnspan=5,
        )
        self.coded_text_box = tk.Text(self.master, width=TEXT_WIDTH, height=TEXT_HEIGHT)
        self.coded_text_box.grid(
            row=self.row + 1,
            column=0,
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
            columnspan=5,
        )
        self.coded_text_box.config(state=tk.NORMAL)

        self.decoded_text_label = tk.Label(self.master, text="Декодированный текст:")
        self.decoded_text_label.grid(
            row=self.row,
            column=6,
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
            sticky="w",
            columnspan=5,
        )
        self.decoded_text_box = tk.Text(
            self.master, width=TEXT_WIDTH, height=TEXT_HEIGHT
        )
        self.decoded_text_box.grid(
            row=self.row + 1,
            column=6,
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
            columnspan=5,
        )
        self.decoded_text_box.config(state=tk.DISABLED)
        self.row += 2

        self.decode_button = tk.Button(
            self.master, text="Декодировать", command=self.decode_text
        )
        self.decode_button.grid(
            row=self.row, column=10, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )

        self.max_iters_label = tk.Label(self.master, text="Максимум итераций:")
        self.max_iters_label.grid(
            row=self.row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.max_iters_entry = tk.Entry(self.master, width=10)
        self.max_iters_entry.grid(
            row=self.row, column=2, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.max_iters_entry.insert(0, "10000")
        self.row += 1

        self.max_best_score_iters_label = tk.Label(
            self.master,
            text="Количество итераций для выхода, при отсутствии улучшений:",
        )
        self.max_best_score_iters_label.grid(
            row=self.row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.max_best_score_iters_entry = tk.Entry(self.master, width=10)
        self.max_best_score_iters_entry.grid(
            row=self.row, column=2, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.max_best_score_iters_entry.insert(0, "500")
        self.row += 1

        self.max_distance_swap_label = tk.Label(
            self.master,
            text="Максимальное расстояние для случайной перестановки ключа:",
        )
        self.max_distance_swap_label.grid(
            row=self.row,
            column=0,
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
            sticky="w",
            columnspan=3,
        )
        self.max_distance_swap_entry = tk.Entry(self.master, width=10)
        self.max_distance_swap_entry.grid(
            row=self.row, column=2, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.max_distance_swap_entry.insert(0, "4")
        self.row += 1

        self.word_impact_factor_label = tk.Label(
            self.master,
            text="Фактор влияния наличия слов из словаря на оценку качества ключа:",
        )
        self.word_impact_factor_label.grid(
            row=self.row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.word_impact_factor_entry = tk.Entry(self.master, width=10)
        self.word_impact_factor_entry.grid(
            row=self.row, column=2, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.word_impact_factor_entry.insert(0, "0.3")
        self.row += 1

        self.min_word_length_label = tk.Label(self.master, text="Мин. длина слова:")
        self.min_word_length_label.grid(
            row=self.row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.min_word_length_entry = tk.Entry(self.master, width=10)
        self.min_word_length_entry.grid(
            row=self.row, column=2, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.min_word_length_entry.insert(0, "3")
        self.row += 1

        self.ngram_choice_label = tk.Label(self.master, text="Выбор оценки:")
        self.ngram_choice_label.grid(
            row=self.row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )

        self.ngram_choice_var = tk.StringVar(value="evaluate_trigrams")

        self.ngram_choice_menu = tk.OptionMenu(
            self.master, self.ngram_choice_var, "evaluate_trigrams", "evaluate_bigrams"
        )
        self.ngram_choice_menu.grid(
            row=self.row, column=2, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.row += 1

    def get_selected_evaluation(self):
        """Функция для получения выбранного значения из меню."""
        return self.ngram_choice_var.get()

    def init_mapping_area(self, row, letter_mapping: dict = None):
        self.key_frame = tk.Frame(self.master, width=self.mapping_width)
        self.key_frame.grid(
            row=row,
            column=0,
            columnspan=5,
            sticky="w",
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
        )
        self.value_frame = tk.Frame(self.master, width=self.mapping_width)
        self.value_frame.grid(
            row=row + 1,
            column=0,
            columnspan=5,
            sticky="w",
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
        )

        self.key_entries = []
        self.value_entries = []

        keys_letter_mapping = list(letter_mapping.keys())
        num_cells = len(keys_letter_mapping)

        cell_width = math.floor(self.mapping_width / num_cells)

        for k in keys_letter_mapping:
            key_entry = tk.Entry(self.key_frame, width=cell_width // 10)
            key_entry.insert(0, k)
            key_entry.config(state=tk.DISABLED)
            key_entry.pack(side=tk.LEFT, padx=1)
            self.key_entries.append(key_entry)

            value_entry = tk.Entry(self.value_frame, width=cell_width // 10)
            value_entry.insert(0, letter_mapping.get(k, "-"))
            value_entry.pack(side=tk.LEFT, padx=1)
            self.value_entries.append(value_entry)

        self.apply_key_button = tk.Button(
            self.master,
            text="Применить ключ",
            command=self.apply_key_mapping,
        )
        self.apply_key_button.grid(
            row=row + 1,
            column=10,
            rowspan=1,
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
            sticky="nsew",
        )

    def apply_key_mapping(self):
        coded_text = self.coded_text_box.get("1.0", tk.END).strip()
        coded_text = self.cipher_cracker.clean_and_format_text(coded_text)
        if coded_text:
            mapping = self.get_mapping()
            decoded_text = self.cipher_cracker.apply_mapping(coded_text, mapping)
            self.insert_decoded_text(decoded_text)

    def get_mapping(self):
        mapping = {
            key_entry.get(): value_entry.get()
            for key_entry, value_entry in zip(self.key_entries, self.value_entries)
        }
        return mapping

    def load_dictionary(self):
        file_path = filedialog.askopenfilename(
            title="Выберите словарь", filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            self.dictionary_entry.delete(0, tk.END)
            self.dictionary_entry.insert(0, file_path)
            self.word_set = self.cipher_cracker.process_file_to_set(file_path)

    def load_open_text(self):
        file_path = filedialog.askopenfilename(
            title="Выберите открытый текст", filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            self.open_text_entry.delete(0, tk.END)
            self.open_text_entry.insert(0, file_path)

            self.open_text = self.cipher_cracker.read_from_file(
                file_name=file_path,
            )

    def insert_decoded_text(self, decoded_text):
        self.decoded_text_box.config(state=tk.NORMAL)
        self.decoded_text_box.delete("1.0", tk.END)
        self.decoded_text_box.insert(tk.END, decoded_text)
        self.decoded_text_box.config(state=tk.DISABLED)

    def decode_text(self):
        coded_text = self.coded_text_box.get("1.0", tk.END).strip()
        if coded_text:
            coded_text = self.cipher_cracker.clean_and_format_text(coded_text)
            max_iters = int(self.max_iters_entry.get())
            max_best_score_iters = int(self.max_best_score_iters_entry.get())
            max_distance_swap = int(self.max_distance_swap_entry.get())
            word_impact_factor = float(self.word_impact_factor_entry.get())
            min_word_length = int(self.min_word_length_entry.get())

            score_function_name = self.get_selected_evaluation()

            letter_mapping = self.cipher_cracker.simple_chrack(
                coded_text=coded_text,
                open_text=self.open_text,
                max_iters=max_iters,
                max_best_score_iters=max_best_score_iters,
                max_distance_swap=max_distance_swap,
                score_function_name=score_function_name,  # "evaluate_bigrams",  # "evaluate_trigrams",  #
                word_set=self.word_set,
                word_impact_factor=word_impact_factor,
                min_word_length=min_word_length,
            )

            decoded_text = self.cipher_cracker.apply_mapping(coded_text, letter_mapping)
            self.init_mapping_area(self.row, letter_mapping=letter_mapping)
            self.insert_decoded_text(decoded_text)


if __name__ == "__main__":
    root = tk.Tk()
    cipher_cracker = CipherCracker()
    cipher_cracker_interface = CipherCrackerInterface(root, cipher_cracker)
    root.mainloop()
