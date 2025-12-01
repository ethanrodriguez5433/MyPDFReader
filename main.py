import tkinter as tk
from tkinter import ttk
import ctypes
from tkinter import filedialog
from pypdf import PdfReader
import threading
import os
from win32com.client import Dispatch
import time

speaker = Dispatch("SAPI.SpVoice")

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

def select_bm():
    global readpath, filename, current_index
    filepath = filedialog.askopenfilename(
        filetypes=[("BM Files", "*.bm")]
    )
    if not filepath:
        return
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    if len(lines) != 2:
        print("invalid .bm file format")
        return

    readpath = lines[0].strip()

    try:
        current_index = int(lines[1].strip())
    except ValueError:
        current_index = 0

    filename = os.path.basename(readpath)
    currently_reading.config(text=f'Currently reading:\n\t"{filename}"')  

def save_bookmark():
    global readpath, current_index, filename
    bm_path = f"bookmarks/{filename}.bm"
    with open(bm_path, "w", encoding="utf-8") as f:
        f.write(f"{readpath}\n{current_index}")

    bookmark_btn.config(image=bookmarkedyes_icon)

def start_reading():
    read_pdf(readpath)

def read_pdf(path):
    global lines, total_lines, current_index, line1, line2, line3, is_playing

    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    lines = text.splitlines()
    total_lines = len(lines)

    while current_index < total_lines:
        if not is_playing:
            break  # stop if paused

        # Update labels
        line1 = lines[current_index] if current_index < total_lines else ""
        line2 = lines[current_index+1] if current_index+1 < total_lines else ""
        line3 = lines[current_index+2] if current_index+2 < total_lines else ""
        label1.config(text=line1)
        label2.config(text=line2)
        label3.config(text=line3)

        current_line = lines[current_index]
        current_words = current_line.split()
        words = len(current_words)
        sleep_time = words / (2)


        # Speak current line
        speaker.Speak(lines[current_index],1)
        time.sleep(sleep_time)
        speaker.Speak("",2) 

        while speaker.Status.RunningState == 2:
            if not is_playing:
                break
            root.update()
        # Increment index and update progress
        current_index += 1
        progress['value'] = (current_index / total_lines) * 100
        root.update_idletasks()

def pause_pdf(path):
    global speaker
    try:
        speaker.Speak("",2)
    except:
        pass
    return

def toggle_play_pause():
    global is_playing, readpath, speaker

    if is_playing:
        play_pause_btn.config(image=play_icon)
        is_playing = False
        speaker.Speak("",2)
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
sidebar = tk.Frame(root, bg="#d9d9d9", width=700)
sidebar.pack(side="left", fill="y")


sidebar.pack_propagate(True)

# -----------------------------------------
# TWO BUTTONS THAT AUTO-FILL VERTICALLY
# -----------------------------------------
select_frame = tk.Frame(sidebar, bg="#C1E5F5")
select_frame.pack(fill="both", expand=True, padx=0, pady=0)

selecticon = tk.PhotoImage(file="icons/selecticon.png")
selectbutton = tk.Button(
    select_frame,
    command=select_pdf,
    image = selecticon,
    bg="#C1E5F5",
    fg="black",
    activebackground="#439FD5",
    activeforeground="white",
    bd=0
)
selectbutton.image = selecticon
selectbutton.pack(fill="both", expand=True)

bm_frame = tk.Frame(sidebar, bg="#C1E5F5")
bm_frame.pack(fill="both", expand=True, padx=0, pady=0)

bookmarkicon = tk.PhotoImage(file="icons/bookmarkicon.png")
bookmarkicon = bookmarkicon.subsample(2,2)
boomarkbutton = tk.Button(
    bm_frame,
    image=bookmarkicon,
    command=select_bm,
    bg="#C1E5F5",
    fg="black",
    activebackground="#439FD5",
    activeforeground="white",
    bd=0)
boomarkbutton.image=bookmarkicon
boomarkbutton.pack(fill="y", expand=True)

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
label1 = tk.Label(reading_frame, text="", bg="white", font=("Aptos(Body)", 35), fg="#439FD5", wraplength=1000)
label2 = tk.Label(reading_frame, text="", bg="white", font=("Aptos(Body)", 35), wraplength=1000)
label3 = tk.Label(reading_frame, text="", bg="white", font=("Aptos(Body)", 35), wraplength=1000)

# Pack labels vertically with spacing
label1.pack(fill="both", expand=True)
label2.pack(fill="both", expand=True)
label3.pack(fill="both", expand=True)
# ------------------------------------------
# Control Panel
# ------------------------------------------
controls_frame = tk.Frame(main_area, bg="white")
controls_frame.pack(side="bottom", fill="x", pady=20)

buttons_frame = tk.Frame(controls_frame, bg="white")
buttons_frame.pack(side="top", pady=10)

#pause/play icon
original_play_icon = tk.PhotoImage(file="icons/play.png")
original_pause_icon = tk.PhotoImage(file="icons/pause.png")

play_icon = original_play_icon.subsample(2,2)
pause_icon = original_pause_icon.subsample(2,2)

is_playing = False

play_pause_btn = tk.Button(
    buttons_frame,
    image=play_icon,
    command=toggle_play_pause,
    bd=0
)
play_pause_btn.pack(side="left",padx=10)

#Bookmark button
original_bookmarked_icon = tk.PhotoImage(file="icons/bookmarked.png")
bookmarked_icon = original_bookmarked_icon.subsample(4,4)

original_bookmarkedyes_icon = tk.PhotoImage(file="icons/bookmarkedyes.png")
bookmarkedyes_icon = original_bookmarkedyes_icon.subsample(4,4)
bookmark_btn = tk.Button(
    buttons_frame,
    command=save_bookmark,
    image=bookmarked_icon,
    bd=0
)
bookmark_btn.pack(side="left", padx=10, pady=40)

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
progress.pack(side="top",pady=10)


root.mainloop()