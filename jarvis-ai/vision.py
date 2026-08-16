import base64
from pathlib import Path

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL


class ScreenVision:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is required for screen vision.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    @staticmethod
    def _data_url(image_path: str | Path) -> str:
        path = Path(image_path)
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        suffix = path.suffix.lower().lstrip(".") or "png"
        mime = "jpeg" if suffix in {"jpg", "jpeg"} else suffix
        return f"data:image/{mime};base64,{encoded}"

    def inspect(self, image_path: str | Path, question: str = "Describe what is visible on my screen and what I can do next.") -> str:
        response = self.client.responses.create(
            model=OPENAI_MODEL,
            instructions=(
                "You are JARVIS screen vision. Analyze only what is visibly present. "
                "Do not claim buttons were clicked or actions happened. If text or UI is uncertain, say so. "
                "Answer in Hinglish or English matching the question."
            ),
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": question},
                        {"type": "input_image", "image_url": self._data_url(image_path)},
                    ],
                }
            ],
        )
        return response.output_text.strip()
