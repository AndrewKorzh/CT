import tkinter as tk

from CipherCracker import CipherCracker
from interface import CipherCrackerInterface


if __name__ == "__main__":
    root = tk.Tk()
    cipher_cracker = CipherCracker()
    cipher_cracker_interface = CipherCrackerInterface(root, cipher_cracker)
    root.mainloop()
