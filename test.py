# save as tts_win32com.py
# Requires: pip install pywin32
from win32com.client import Dispatch

def speak_words(words):
    speaker = Dispatch("SAPI.SpVoice")
    # Synchronous speaking (blocks until finished)
    for w in words:
        speaker.Speak(w)     # blocks until w finishes

if __name__ == "__main__":
    speak_words(["hello", "world", "this", "is", "a", "test"])
