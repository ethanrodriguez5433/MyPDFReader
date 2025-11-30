import tkinter as tk
from tkinter import ttk
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

        progress_percent = (current_index/total_lines) * 100
        progress['value'] = progress_percent
        root.update_idletasks()

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


###########################################
# LEFT SIDEBAR (fixed width, full height)
###########################################
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

############################################
# MAIN AREA
############################################
main_area = tk.Frame(root, bg="white")
main_area.pack(side="right", fill="both", expand=True)

# ------------------------------------------
# Information Frame
# ------------------------------------------
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

# -------------------------------------------
# Reading Frame
# -------------------------------------------
reading_frame = tk.Frame(
    main_area,
    bg="white",
    highlightbackground="black",
    highlightthickness=10
)
reading_frame.pack(side="top",
                   fill="both",
                   expand=True,
                   pady=20,
                   padx=220)

# Inside the middle frame, add 3 labels
label1 = tk.Label(reading_frame, text="line1", bg="white", font=("Aptos(Body)", 35), fg="#439FD5")
label2 = tk.Label(reading_frame, text="line2", bg="white", font=("Aptos(Body)", 35))
label3 = tk.Label(reading_frame, text="line3", bg="white", font=("Aptos(Body)", 35))

# Pack labels vertically with spacing
label1.pack(fill="both", expand=True)
label2.pack(fill="both", expand=True)
label3.pack(fill="both", expand=True)
# ------------------------------------------
# Control Panel
# ------------------------------------------
controls_frame = tk.Frame(main_area, bg="white")
controls_frame.pack(side="bottom", fill="x", pady=20)

#pause/play icon
original_play_icon = tk.PhotoImage(file="icons/play.png")
original_pause_icon = tk.PhotoImage(file="icons/pause.png")

play_icon = original_play_icon.subsample(4,4)
pause_icon = original_pause_icon.subsample(4,4)

is_playing = False

play_pause_btn = tk.Button(
    controls_frame,
    image=play_icon,
    command=toggle_play_pause,
    bd=0
)
play_pause_btn.pack(pady=40)

#Progress bar
style = ttk.Style()
style.theme_use('default')
style.configure(
    "Custom.Horizontal.TProgressbar",
    throughcolor="#C1E5F5",
    background="#439FD5",
    thickness=50
)
progress = tk.ttk.Progressbar(controls_frame, 
                              orient = "horizontal",
                              length = 1000, 
                              mode = "determinate", 
                              maximum=100,
                              style="Custom.Horizontal.TProgressbar")
progress.pack(pady=10)


root.mainloop()