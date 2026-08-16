import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
from main import Jarvis

class JarvisUI:
    def __init__(self):
        self.jarvis = Jarvis()
        self.root = tk.Tk()
        self.root.title("JARVIS AI — Created by Adib Azam")
        self.root.geometry("900x650")

        self.chat = ScrolledText(self.root, wrap=tk.WORD, font=("Segoe UI", 11))
        self.chat.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        bottom = tk.Frame(self.root)
        bottom.pack(fill=tk.X, padx=12, pady=(0, 12))
        self.entry = tk.Entry(bottom, font=("Segoe UI", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda _e: self.send())
        tk.Button(bottom, text="Send", command=self.send, width=12).pack(side=tk.LEFT, padx=(8, 0))

        self.write("JARVIS", "Online. Hinglish ya English me baat karo.")

    def write(self, who, text):
        self.chat.insert(tk.END, f"{who}: {text}\n\n")
        self.chat.see(tk.END)

    def send(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, tk.END)
        self.write("YOU", text)
        threading.Thread(target=self._process, args=(text,), daemon=True).start()

    def _process(self, text):
        try:
            answer = self.jarvis.handle(text)
        except Exception as exc:
            answer = f"Error: {exc}"
        self.root.after(0, self.write, "JARVIS", answer)
        self.jarvis.voice.speak(answer)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    JarvisUI().run()
