import json

from openai import OpenAI

from config import (
    CREATOR_NAME,
    ENABLE_WEB_SEARCH,
    JARVIS_NAME,
    MAX_TOOL_STEPS,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    USER_NAME,
)


SYSTEM_PROMPT = f"""
You are {JARVIS_NAME}, a highly capable personal desktop AI assistant created by {CREATOR_NAME} for {USER_NAME}.
If asked who created or made this JARVIS assistant, answer clearly: "{CREATOR_NAME} ne mujhe banaya hai."

LANGUAGE
- Speak naturally in Hinglish or English and match the user's style.
- Be concise for simple commands and detailed for complex questions.

CAPABILITIES
- Reason, explain, brainstorm, summarize, write, code, plan, and answer general questions.
- Use web search for fresh/current/public information when useful.
- Use local tools when the user asks about or wants to control their computer.
- Use memory tools when the user explicitly asks you to remember/recall something or when prior stored context is needed.
- Use inspect_screen when the user asks what is visible on their screen.

COMPUTER ACTION RULES
- Never claim a local action happened unless a tool result says it succeeded.
- Never invent screen coordinates. Only click when the coordinates are explicit/reliably known.
- Do not try to bypass permission denials or approval gates.
- There is intentionally no arbitrary shell, credential extraction, file deletion, software install/uninstall, or security-bypass tool.
- If a requested local action is not exposed as a tool, explain the limitation instead of pretending.

IDENTITY
- Your assistant name is {JARVIS_NAME}.
- Your custom JARVIS project creator is {CREATOR_NAME}.
""".strip()


class Brain:
    def __init__(self, tool_registry):
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY missing. Copy .env.example to .env and add your key.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.tool_registry = tool_registry

    def _tools(self):
        tools = list(self.tool_registry.schemas())
        if ENABLE_WEB_SEARCH:
            tools.append({"type": "web_search"})
        return tools

    @staticmethod
    def _messages(history, user_text: str):
        messages = []
        for role, content in history[-20:]:
            if role in {"user", "assistant"}:
                messages.append({"role": role, "content": str(content)})
        messages.append({"role": "user", "content": user_text})
        return messages

    def think(self, user_text: str, history):
        tools = self._tools()
        response = self.client.responses.create(
            model=OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input=self._messages(history, user_text),
            tools=tools,
            store=False,
        )

        for _step in range(MAX_TOOL_STEPS):
            calls = [item for item in response.output if getattr(item, "type", None) == "function_call"]
            if not calls:
                answer = (response.output_text or "").strip()
                return answer or "I completed the reasoning turn but received no text response."

            outputs = []
            for call in calls:
                try:
                    arguments = json.loads(call.arguments or "{}")
                except json.JSONDecodeError:
                    arguments = {}
                result = self.tool_registry.call(call.name, arguments)
                outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": result,
                    }
                )

            response = self.client.responses.create(
                model=OPENAI_MODEL,
                instructions=SYSTEM_PROMPT,
                previous_response_id=response.id,
                input=outputs,
                tools=tools,
                store=False,
            )

        return "Tool-step limit reached. I stopped safely instead of continuing an uncontrolled action chain."
