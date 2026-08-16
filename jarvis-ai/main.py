from brain import Brain
from computer import ComputerController
from listen import Listener
from memory import Memory
from tools import ToolRegistry
from voice import Voice


class Jarvis:
    def __init__(self, confirm_callback=None):
        self.memory = Memory()
        self.computer = ComputerController()
        self.voice = Voice()
        self.listener = Listener()
        self.confirm_callback = confirm_callback or self._terminal_confirm
        self.tools = ToolRegistry(self.computer, self.memory, self.confirm_callback)
        self.brain = Brain(self.tools)

    @staticmethod
    def _terminal_confirm(tool_name: str, arguments: dict) -> bool:
        print(f"\nJARVIS permission request > {tool_name} {arguments}")
        answer = input("Allow this action? [y/N]: ").strip().lower()
        return answer in {"y", "yes"}

    def handle(self, text: str):
        text = str(text).strip()
        if not text:
            return ""
        history = self.memory.recent(20)
        self.memory.add("user", text)
        answer = self.brain.think(text, history)
        self.memory.add("assistant", answer)
        return answer

    def voice_command_once(self):
        print("Listening...")
        text = self.listener.listen_once()
        print(f"You > {text}")
        answer = self.handle(text)
        self.voice.speak(answer)
        return answer

    def wake_word_mode(self):
        print("Wake-word mode active. Say 'Hey JARVIS' or 'JARVIS'. Ctrl+C to stop.")
        while True:
            command = self.listener.wait_for_wake_word()
            if not command:
                self.voice.speak("Yes, Adib?")
                try:
                    command = self.listener.listen_once(timeout=6, phrase_time_limit=25)
                except Exception:
                    continue
            print(f"You > {command}")
            if command.lower() in {"exit", "quit", "goodbye", "stop jarvis"}:
                self.voice.speak("Goodbye, Adib.")
                return
            try:
                answer = self.handle(command)
            except Exception as exc:
                answer = f"Error: {exc}"
            print(f"JARVIS > {answer}")
            self.voice.speak(answer)


def cli():
    jarvis = Jarvis()
    print("JARVIS V2 online — created by Adib Azam.")
    print("Commands: /voice = one voice command, /wake = wake-word mode, /clear = clear chat memory, exit = stop")

    while True:
        text = input("You > ").strip()
        if not text:
            continue
        if text.lower() in {"exit", "quit", "bye"}:
            print("JARVIS > Goodbye, Adib.")
            break
        if text.lower() == "/voice":
            try:
                answer = jarvis.voice_command_once()
                print(f"JARVIS > {answer}")
            except Exception as exc:
                print(f"JARVIS voice error > {exc}")
            continue
        if text.lower() == "/wake":
            try:
                jarvis.wake_word_mode()
            except KeyboardInterrupt:
                print("\nWake-word mode stopped.")
            continue
        if text.lower() == "/clear":
            jarvis.memory.clear_conversation()
            print("JARVIS > Conversation memory cleared. Long-term facts were kept.")
            continue

        try:
            answer = jarvis.handle(text)
            print(f"JARVIS > {answer}")
            jarvis.voice.speak(answer)
        except Exception as exc:
            print(f"JARVIS error > {exc}")


if __name__ == "__main__":
    cli()
