import tkinter as tk
from tkinter import filedialog
# Import necessary libraries

def select_file_path():

    root = tk.Tk()
    root.withdraw()
    # Initializes and displays file browser selection window

    root.attributes('-topmost', True)
    # Orders the file explorer prompt window to appear above over every other window

    directory_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Images", "*.png;*.jpg;*.jpeg")],
        initialdir="/")
    # Assigns selected file to a string

    root.destroy()
    # Destroys the prompt window after a file is selected

    return directory_path
    # Returns a string containing the absolute path of the selected file