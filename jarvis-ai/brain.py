import json
import re
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, CREATOR_NAME, JARVIS_NAME

SYSTEM_PROMPT = f"""
You are {JARVIS_NAME}, an advanced personal AI assistant created by {CREATOR_NAME}.
If asked who created/made you, answer clearly: '{CREATOR_NAME} ne mujhe banaya hai.'
Speak naturally in Hinglish or English, matching the user's language.
Be highly capable: answer questions, explain, plan, code, reason, summarize, brainstorm, and assist with computer tasks.
Never claim an action happened unless a tool actually executed it.
For computer actions return ONLY a JSON object in this exact schema:
{{"action":"open_app|type_text|hotkey|screenshot|lock_pc|none","args":[],"message":"short response"}}
Use 'none' for normal conversation. Destructive, financial, credential, privacy-sensitive, install/uninstall, delete, send/post, or system-changing operations must not be invented or bypass confirmation.
"""

class Brain:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY missing. Copy .env.example to .env and add your key.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def think(self, user_text: str, history):
        context = "\n".join(f"{role}: {content}" for role, content in history[-12:])
        prompt = f"Conversation history:\n{context}\n\nUser: {user_text}"
        response = self.client.responses.create(
            model=OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input=prompt,
        )
        text = response.output_text.strip()
        return self._parse(text)

    def _parse(self, text: str):
        try:
            data = json.loads(text)
            if isinstance(data, dict) and "action" in data:
                return data
        except json.JSONDecodeError:
            pass
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            try:
                data = json.loads(match.group(0))
                if "action" in data:
                    return data
            except json.JSONDecodeError:
                pass
        return {"action": "none", "args": [], "message": text}
