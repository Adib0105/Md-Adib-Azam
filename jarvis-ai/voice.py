import queue
import threading

import pyttsx3


class Voice:
    def __init__(self, rate=180):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.queue = queue.Queue()
        self.worker = threading.Thread(target=self._loop, daemon=True)
        self.worker.start()

    def speak(self, text: str):
        text = str(text).strip()
        if text:
            self.queue.put(text)

    def _loop(self):
        while True:
            text = self.queue.get()
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass
            finally:
                self.queue.task_done()
