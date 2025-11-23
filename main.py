import tkinter as tk
import ctypes
from tkinter import filedialog
import pyttsx3
from pypdf import PdfReader

engine = pyttsx3.init()

def select_pdf():
    filepath = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not filepath:
        return
    read_pdf(filepath)

def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    engine.say(text)
    engine.runAndWait()

# Fix blurry window on Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

root = tk.Tk()
root.title("PDF Reader")
root.geometry("450x250")
root.tk.call('tk','scaling', 1.3)

button = tk.Button(root, text="Select PDF", command=select_pdf)
button.pack(padx=20, pady=20)

root.mainloop()