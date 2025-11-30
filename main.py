import tkinter as tk
import ctypes
from tkinter import filedialog
import pyttsx3
from pypdf import PdfReader
import threading
import os

engine = pyttsx3.init()

filename = "No file selected"

current_index = 0
total_lines = 0
line1 = "" 
line2= ""
line3 = ""
lines = []

#-----------------------------------
# Functionality
#----------------------------------

def select_pdf():
    global readpath
    global filename
    filepath = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not filepath:
        return
    readpath = filepath

    filename = os.path.basename(filepath)
    currently_reading.config(text=f'Currently reading:\n\t"{filename}"')

def start_reading():
    read_pdf(readpath)

def read_pdf(path):
    global lines, total_lines, current_index, line1, line2, line3

    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    lines = text.splitlines()
    total_lines = len(lines)

    def update_line_window():
        global line1, line2, line3
        line1 = lines[current_index] if current_index < total_lines else ""
        line2 = lines[current_index+1] if current_index+1 < total_lines else ""
        line3 = lines[current_index+2] if current_index+2 < total_lines else ""
    
    update_line_window()

    while current_index < total_lines:
        engine.say(lines[current_index])
        engine.runAndWait()

        current_index += 1
        update_line_window()

def pause_pdf(path):
    global engine
    try:
        engine.stop()
    except:
        pass
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

#-----------------------------------------
# UI
#-----------------------------------------

# Fix blurry window on Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

root = tk.Tk()
root.title("PDF Reader")
root.geometry("1920x1200")
root.config(bg="skyblue")
root.tk.call('tk','scaling', 1.3)


# -----------------------------------------
# LEFT SIDEBAR (fixed width, full height)
# -----------------------------------------
sidebar = tk.Frame(root, bg="#d9d9d9", width=550)
sidebar.pack(side="left", fill="y")


sidebar.pack_propagate(True)

# -----------------------------------------
# TWO BUTTONS THAT AUTO-FILL VERTICALLY
# -----------------------------------------
selecticon = tk.PhotoImage(file="icons/selecticon.png")
selectbutton = tk.Button(
    sidebar,
    command=select_pdf,
    image = selecticon,
    bg="#C1E5F5",
    fg="black",
    activebackground="#439FD5",
    activeforeground="white",
    bd=0                   #(flat look)
)
selectbutton.image = selecticon
selectbutton.pack(fill="both", expand=True)

bookmarkicon = tk.PhotoImage(file="icons/bookmarkicon.png")
boomarkbutton = tk.Button(
    sidebar,
    image=bookmarkicon,
    command=select_pdf,
    bg="#C1E5F5",
    fg="black",
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

information_frame = tk.Frame(main_area, bg="white")
information_frame.pack(side="top", fill="x", pady=20)

currently_reading = tk.Label(information_frame,
                             text=f"Currently reading:\n\tNo file currently selected",
                             bg="White",
                             font=("Aptos(Body)",50,"bold"),
                             anchor="w",
                             justify="left",
                             padx=50)
currently_reading.pack(fill="x")

original_play_icon = tk.PhotoImage(file="icons/play.png")
original_pause_icon = tk.PhotoImage(file="icons/pause.png")

play_icon = original_play_icon.subsample(2,2)
pause_icon = original_pause_icon.subsample(2,2)

is_playing = False
controls_frame = tk.Frame(main_area, bg="white")
controls_frame.pack(side="bottom", fill="x", pady=20)

play_pause_btn = tk.Button(
    controls_frame,
    image=play_icon,
    command=toggle_play_pause,
    bd=0
)
play_pause_btn.pack(pady=40)

root.mainloop()