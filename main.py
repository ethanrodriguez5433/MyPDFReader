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
root.geometry("800x500")
root.config(bg="skyblue")
root.tk.call('tk','scaling', 1.3)


# -----------------------------------------
# LEFT SIDEBAR (fixed width, full height)
# -----------------------------------------
sidebar = tk.Frame(root, bg="#d9d9d9", width=550)
sidebar.pack(side="left", fill="y")

# Make the frame enforce its width even when children expand
sidebar.pack_propagate(False)

# -----------------------------------------
# TWO BUTTONS THAT AUTO-FILL VERTICALLY
# -----------------------------------------
selecticon = tk.PhotoImage(file="selecticon.png")
btn1 = tk.Button(
    sidebar,
    command=select_pdf,
    image = selecticon,
    bg="#C1E5F5",          # green
    fg="black",            # white text
    activebackground="#439FD5",
    activeforeground="white",
    bd=0                   # optional (flat look)
)
btn1.image = selecticon
btn1.pack(fill="both", expand=True)

bookmarkicon = tk.PhotoImage(file="bookmarkicon.png")
btn2 = tk.Button(
    sidebar,
    image=bookmarkicon,
    command=select_pdf,
    bg="#C1E5F5",          # green
    fg="black",            # white text
    activebackground="#439FD5",
    activeforeground="white",
    bd=0)
btn2.image=bookmarkicon
btn2.pack(fill="both", expand=True)

# -----------------------------------------
# MAIN AREA
# -----------------------------------------
main_area = tk.Frame(root, bg="white")
main_area.pack(side="right", fill="both", expand=True)

root.mainloop()