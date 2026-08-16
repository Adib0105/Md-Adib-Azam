import threading
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from main import Jarvis


class JarvisUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS V2 — Created by Adib Azam")
        self.root.geometry("980x700")
        self.root.minsize(760, 520)

        self.jarvis = Jarvis(confirm_callback=self.confirm_action)

        header = tk.Frame(self.root)
        header.pack(fill=tk.X, padx=12, pady=(12, 0))
        tk.Label(header, text="JARVIS V2", font=("Segoe UI", 18, "bold")).pack(side=tk.LEFT)
        tk.Label(header, text="  •  Adib Azam AI Assistant", font=("Segoe UI", 10)).pack(side=tk.LEFT)

        self.status = tk.StringVar(value="ONLINE")
        tk.Label(header, textvariable=self.status, font=("Segoe UI", 10, "bold")).pack(side=tk.RIGHT)

        self.chat = ScrolledText(self.root, wrap=tk.WORD, font=("Segoe UI", 11))
        self.chat.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        bottom = tk.Frame(self.root)
        bottom.pack(fill=tk.X, padx=12, pady=(0, 12))

        self.entry = tk.Entry(bottom, font=("Segoe UI", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda _e: self.send())

        tk.Button(bottom, text="Voice", command=self.voice_once, width=10).pack(side=tk.LEFT, padx=(8, 0))
        tk.Button(bottom, text="Send", command=self.send, width=10).pack(side=tk.LEFT, padx=(8, 0))

        self.write("JARVIS", "V2 online. Hinglish ya English me baat karo. Main web, memory, screen vision aur approved PC tools use kar sakta hoon.")
        self.entry.focus_set()

    def write(self, who, text):
        self.chat.insert(tk.END, f"{who}: {text}\n\n")
        self.chat.see(tk.END)

    def set_status(self, text):
        self.status.set(text)

    def confirm_action(self, tool_name: str, arguments: dict) -> bool:
        done = threading.Event()
        result = {"allowed": False}

        def ask():
            result["allowed"] = messagebox.askyesno(
                "JARVIS Permission",
                f"JARVIS wants to run:\n\n{tool_name}\n{arguments}\n\nAllow this action?",
                parent=self.root,
            )
            done.set()

        self.root.after(0, ask)
        done.wait()
        return result["allowed"]

    def send(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, tk.END)
        self.write("YOU", text)
        self.set_status("THINKING")
        threading.Thread(target=self._process, args=(text,), daemon=True).start()

    def _process(self, text):
        try:
            answer = self.jarvis.handle(text)
        except Exception as exc:
            answer = f"Error: {exc}"
        self.root.after(0, self.write, "JARVIS", answer)
        self.root.after(0, self.set_status, "ONLINE")
        self.jarvis.voice.speak(answer)

    def voice_once(self):
        self.set_status("LISTENING")
        threading.Thread(target=self._voice_worker, daemon=True).start()

    def _voice_worker(self):
        try:
            text = self.jarvis.listener.listen_once()
            self.root.after(0, self.write, "YOU (VOICE)", text)
            self.root.after(0, self.set_status, "THINKING")
            answer = self.jarvis.handle(text)
        except Exception as exc:
            answer = f"Voice error: {exc}"
        self.root.after(0, self.write, "JARVIS", answer)
        self.root.after(0, self.set_status, "ONLINE")
        self.jarvis.voice.speak(answer)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    JarvisUI().run()
