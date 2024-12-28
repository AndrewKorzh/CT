import tkinter as tk
from tkinter import filedialog, messagebox
from TextHandler import TextHandler
from CipherCracker import CipherCracker
import math

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

        self.init_ui()

    def init_ui(self):
        row = 0
        self.open_text_label = tk.Label(self.master, text="Открытый текст:")
        self.open_text_label.grid(
            row=row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.open_text_entry = tk.Entry(
            self.master,
            width=math.floor(TEXT_WIDTH * 2),
        )
        self.open_text_entry.grid(
            row=row, column=1, padx=DEFAULT_PADX, pady=DEFAULT_PADY, columnspan=9
        )
        self.load_button = tk.Button(
            self.master, text="Загрузить", command=self.load_open_text
        )
        self.load_button.grid(row=row, column=10, padx=DEFAULT_PADX, pady=DEFAULT_PADY)
        row += 1

        # Словарь
        self.dictionary_label = tk.Label(self.master, text="Словарь (не обязательно):")
        self.dictionary_label.grid(
            row=row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.dictionary_entry = tk.Entry(self.master, width=math.floor(TEXT_WIDTH * 2))
        self.dictionary_entry.grid(
            row=row,
            column=1,
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
            columnspan=9,
        )
        self.load_dict_button = tk.Button(
            self.master, text="Загрузить словарь", command=self.load_dictionary
        )
        self.load_dict_button.grid(
            row=row, column=10, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )

        row += 1

        # Окно для закодированного текста
        self.coded_text_label = tk.Label(self.master, text="Закодированный текст:")
        self.coded_text_label.grid(
            row=row,
            column=0,
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
            sticky="w",
            columnspan=5,
        )
        self.coded_text_box = tk.Text(self.master, width=TEXT_WIDTH, height=TEXT_HEIGHT)
        self.coded_text_box.grid(
            row=row + 1, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, columnspan=5
        )
        self.coded_text_box.config(state=tk.NORMAL)

        self.decoded_text_label = tk.Label(self.master, text="Декодированный текст:")
        self.decoded_text_label.grid(
            row=row,
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
            row=row + 1,
            column=6,
            padx=DEFAULT_PADX,
            pady=DEFAULT_PADY,
            columnspan=5,
        )
        self.decoded_text_box.config(state=tk.DISABLED)
        row += 2

        # Параметры декодирования с значениями по умолчанию
        self.max_iters_label = tk.Label(self.master, text="Макс. итераций:")
        self.max_iters_label.grid(
            row=row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.max_iters_entry = tk.Entry(self.master, width=10)
        self.max_iters_entry.grid(
            row=row, column=1, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.max_iters_entry.insert(0, "10000")  # Значение по умолчанию
        row += 1

        self.max_best_score_iters_label = tk.Label(
            self.master, text="Макс. итераций для лучшего результата:"
        )
        self.max_best_score_iters_label.grid(
            row=row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.max_best_score_iters_entry = tk.Entry(self.master, width=10)
        self.max_best_score_iters_entry.grid(
            row=row, column=1, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.max_best_score_iters_entry.insert(0, "500")  # Значение по умолчанию
        row += 1

        self.max_distance_swap_label = tk.Label(
            self.master, text="Макс. расстояние для перестановки:"
        )
        self.max_distance_swap_label.grid(
            row=row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.max_distance_swap_entry = tk.Entry(self.master, width=10)
        self.max_distance_swap_entry.grid(
            row=row, column=1, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.max_distance_swap_entry.insert(0, "4")  # Значение по умолчанию
        row += 1

        self.word_impact_factor_label = tk.Label(
            self.master, text="Фактор влияния слов:"
        )
        self.word_impact_factor_label.grid(
            row=row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.word_impact_factor_entry = tk.Entry(self.master, width=10)
        self.word_impact_factor_entry.grid(
            row=row, column=1, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.word_impact_factor_entry.insert(0, "0.3")  # Значение по умолчанию
        row += 1

        self.min_word_length_label = tk.Label(self.master, text="Мин. длина слова:")
        self.min_word_length_label.grid(
            row=row, column=0, padx=DEFAULT_PADX, pady=DEFAULT_PADY, sticky="w"
        )
        self.min_word_length_entry = tk.Entry(self.master, width=10)
        self.min_word_length_entry.grid(
            row=row, column=1, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        self.min_word_length_entry.insert(0, "3")  # Значение по умолчанию
        row += 1

        # Кнопка для декодирования
        self.decode_button = tk.Button(
            self.master, text="Декодировать", command=self.decode_text
        )
        self.decode_button.grid(
            row=row + 1, column=10, padx=DEFAULT_PADX, pady=DEFAULT_PADY
        )
        row += 1

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

    def decode_text(self):
        coded_text = self.coded_text_box.get("1.0", tk.END).strip()
        if coded_text:

            max_iters = int(self.max_iters_entry.get())
            max_best_score_iters = int(self.max_best_score_iters_entry.get())
            max_distance_swap = int(self.max_distance_swap_entry.get())
            word_impact_factor = float(self.word_impact_factor_entry.get())
            min_word_length = int(self.min_word_length_entry.get())

            decoded_text = self.cipher_cracker.simple_chrack(
                coded_text=coded_text,
                open_text=self.open_text,
                max_iters=max_iters,
                max_best_score_iters=max_best_score_iters,
                max_distance_swap=max_distance_swap,
                score_function_name="evaluate_trigrams",
                word_set=self.word_set,
                word_impact_factor=word_impact_factor,
                min_word_length=min_word_length,
            )

            self.decoded_text_box.config(state=tk.NORMAL)
            self.decoded_text_box.delete("1.0", tk.END)
            self.decoded_text_box.insert(tk.END, decoded_text)
            self.decoded_text_box.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    cipher_cracker = CipherCracker()
    cipher_cracker_interface = CipherCrackerInterface(root, cipher_cracker)
    root.mainloop()
