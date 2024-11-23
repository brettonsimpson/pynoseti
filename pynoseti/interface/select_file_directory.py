import tkinter as tk
from tkinter import filedialog
# Import necessary libraries

def select_file_directory():

    root = tk.Tk()
    root.withdraw()
    # Initializes and displays file directory selection window

    root.attributes('-topmost', True)
    # Orders the file explorer prompt window to appear above over every other window

    directory_path = filedialog.askdirectory()
    # Assigns selected folder to a string

    root.destroy()
    # Destroys the prompt window after a directory is selected

    return directory_path
    # Returns a string containing the absolute path of the selected directory