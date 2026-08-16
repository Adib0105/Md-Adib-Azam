from brain import Brain
from computer import ComputerController
from memory import Memory
from voice import Voice
from config import REQUIRE_CONFIRMATION

RISKY_ACTIONS = {"type_text", "hotkey", "lock_pc"}

class Jarvis:
    def __init__(self):
        self.brain = Brain()
        self.computer = ComputerController()
        self.memory = Memory()
        self.voice = Voice()

    def handle(self, text: str):
        self.memory.add("user", text)
        plan = self.brain.think(text, self.memory.recent())
        action = plan.get("action", "none")
        args = plan.get("args", []) or []
        message = plan.get("message", "")

        if action == "none":
            answer = message
        else:
            if REQUIRE_CONFIRMATION and action in RISKY_ACTIONS:
                confirm = input(f"JARVIS wants to run {action} {args}. Allow? [y/N]: ").strip().lower()
                if confirm not in {"y", "yes"}:
                    answer = "Action cancelled."
                    self.memory.add("assistant", answer)
                    return answer
            answer = self.execute(action, args)
            if message:
                answer = f"{message}\n{answer}"

        self.memory.add("assistant", answer)
        return answer

    def execute(self, action, args):
        handlers = {
            "open_app": self.computer.open_app,
            "type_text": self.computer.type_text,
            "hotkey": self.computer.hotkey,
            "screenshot": self.computer.screenshot,
            "lock_pc": self.computer.lock_pc,
        }
        fn = handlers.get(action)
        if not fn:
            return f"Unknown action: {action}"
        return fn(*args)


def cli():
    jarvis = Jarvis()
    print("JARVIS online. Type 'exit' to stop.")
    while True:
        text = input("You > ").strip()
        if not text:
            continue
        if text.lower() in {"exit", "quit", "bye"}:
            print("JARVIS > Goodbye, Adib.")
            break
        try:
            answer = jarvis.handle(text)
            print(f"JARVIS > {answer}")
            jarvis.voice.speak(answer)
        except Exception as exc:
            print(f"JARVIS error > {exc}")


if __name__ == "__main__":
    cli()
