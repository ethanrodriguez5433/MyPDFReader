import tkinter as tk
import ctypes
from tkinter import filedialog
import pyttsx3
from pypdf import PdfReader
import threading

engine = pyttsx3.init()


def select_pdf():
    global readpath
    filepath = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not filepath:
        return
    readpath = filepath
    #read_pdf(filepath)

def start_reading():
    read_pdf(readpath)

def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    engine.say(text)
    engine.runAndWait()

def pause_pdf(path):
    engine.stop()
    return

def toggle_play_pause():
    global is_playing, readpath

    if is_playing:
        play_pause_btn.config(image=play_icon)
        is_playing = False
        engine.stop()
        return

    else:
        if "readpath" not in globals():
            print("No PDF selected yet.")
            return
        play_pause_btn.config(image=pause_icon)
        is_playing = True

        
        t = threading.Thread(target=start_reading)
        t.daemon = True
        t.start()
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
selecticon = tk.PhotoImage(file="icons/selecticon.png")
selectbutton = tk.Button(
    sidebar,
    command=select_pdf,
    image = selecticon,
    bg="#C1E5F5",          # green
    fg="black",            # white text
    activebackground="#439FD5",
    activeforeground="white",
    bd=0                   # optional (flat look)
)
selectbutton.image = selecticon
selectbutton.pack(fill="both", expand=True)

bookmarkicon = tk.PhotoImage(file="icons/bookmarkicon.png")
boomarkbutton = tk.Button(
    sidebar,
    image=bookmarkicon,
    command=select_pdf,
    bg="#C1E5F5",          # green
    fg="black",            # white text
    activebackground="#439FD5",
    activeforeground="white",
    bd=0)
boomarkbutton.image=bookmarkicon
boomarkbutton.pack(fill="both", expand=True)

# -----------------------------------------
# MAIN AREA
# -----------------------------------------
main_area = tk.Frame(root, bg="white")
main_area.pack(side="right", fill="both", expand=True)

play_icon = tk.PhotoImage(file="icons/play.png")
pause_icon = tk.PhotoImage(file="icons/pause.png")

is_playing = False

play_pause_btn = tk.Button(
    main_area,
    image=play_icon,
    command=toggle_play_pause,
    bd=0
)
play_pause_btn.pack(pady=40)

root.mainloop()