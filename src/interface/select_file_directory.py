import tkinter as tk
from tkinter import filedialog

def select_directory():

    root = tk.Tk()

    root.withdraw()

    directory_path = filedialog.askdirectory()

    return directory_path