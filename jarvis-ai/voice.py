import threading
import pyttsx3

class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 180)

    def speak(self, text: str):
        def _run():
            self.engine.say(text)
            self.engine.runAndWait()
        threading.Thread(target=_run, daemon=True).start()
