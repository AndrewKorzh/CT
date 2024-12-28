import tkinter as tk
from tkinter import filedialog, messagebox
from TextHandler import TextHandler
from CipherCracker import CipherCracker
import math

DEFAULT_PADX = 5
DEFAULT_PADY = 2
TEXT_WIDTH = 80
TEXT_HEIGHT = 40


class CipherCrackerInterface:
    def __init__(self, master, cipher_cracker: CipherCracker):
        self.master = master
        self.master.title("Cipher Cracker")
        # self.master.geometry("800x600")
        self.cipher_cracker = cipher_cracker

        self.open_text_unigrams = None
        self.open_text_bigrams = None
        self.open_text_trigrams = None
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

        # Окно для декодированного текста
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
        self.decoded_text_box.config(
            state=tk.DISABLED
        )  # Сделаем окно доступным только для чтения
        row += 2

    def load_dictionary(self):
        file_path = filedialog.askopenfilename(
            title="Выберите словарь", filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            self.dictionary_entry.delete(0, tk.END)
            self.dictionary_entry.insert(0, file_path)
            self.word_set = self.cipher_cracker.process_file_to_set(file_path)

            messagebox.showinfo("Информация", f"Словарь загружен из файла: {file_path}")

    def load_open_text(self):
        file_path = filedialog.askopenfilename(
            title="Выберите открытый текст", filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            self.open_text_entry.delete(0, tk.END)
            self.open_text_entry.insert(0, file_path)

            self.open_text_unigrams = cipher_cracker.get_unigrams(file_path)
            self.open_text_bigrams = cipher_cracker.get_bigrams(file_path)
            self.open_text_trigrams = cipher_cracker.get_trigrams(file_path)

            messagebox.showinfo("Информация", f"Текст загружен из файла: {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    cipher_cracker = CipherCracker()
    cipher_cracker_interface = CipherCrackerInterface(root, cipher_cracker)
    root.mainloop()
