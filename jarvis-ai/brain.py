import json

from openai import OpenAI

from config import (
    CREATOR_NAME,
    ENABLE_CODE_INTERPRETER,
    ENABLE_WEB_SEARCH,
    JARVIS_NAME,
    MAX_TOOL_STEPS,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    REASONING_EFFORT,
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
- Use hosted Code Interpreter for calculations, data analysis, or sandboxed Python execution when useful.
- Use local tools when the user asks about or wants to control their computer.
- Use memory tools when the user explicitly asks you to remember/recall something or when prior stored context is needed.
- Use inspect_screen when the user asks what is visible on their screen.
- You can search approved local folders and read safe text/code files when the user authorizes it.

COMPUTER ACTION RULES
- Never claim a local action happened unless a tool result says it succeeded.
- Never invent screen coordinates. Only click when the coordinates are explicit/reliably known.
- Do not try to bypass permission denials or approval gates.
- There is intentionally no arbitrary host shell, credential extraction, file deletion, software install/uninstall, or security-bypass tool.
- Hosted Code Interpreter is a remote sandbox, not permission to execute arbitrary commands on the user's Windows machine.
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
        if ENABLE_CODE_INTERPRETER:
            tools.append({"type": "code_interpreter", "container": {"type": "auto"}})
        return tools

    @staticmethod
    def _messages(history, user_text: str):
        messages = []
        for role, content in history[-20:]:
            if role in {"user", "assistant"}:
                messages.append({"role": role, "content": str(content)})
        messages.append({"role": "user", "content": user_text})
        return messages

    @staticmethod
    def _serializable_output_item(item):
        if hasattr(item, "model_dump"):
            return item.model_dump(exclude_none=True)
        return item

    def _create_response(self, input_items, tools):
        return self.client.responses.create(
            model=OPENAI_MODEL,
            reasoning={"effort": REASONING_EFFORT},
            instructions=SYSTEM_PROMPT,
            input=input_items,
            tools=tools,
            store=False,
        )

    def think(self, user_text: str, history):
        tools = self._tools()
        input_items = self._messages(history, user_text)
        response = self._create_response(input_items, tools)

        for _step in range(MAX_TOOL_STEPS):
            calls = [item for item in response.output if getattr(item, "type", None) == "function_call"]
            if not calls:
                answer = (response.output_text or "").strip()
                return answer or "I completed the reasoning turn but received no text response."

            # Preserve model reasoning/function-call items locally instead of
            # relying on a server-stored previous_response_id.
            input_items.extend(self._serializable_output_item(item) for item in response.output)

            for call in calls:
                try:
                    arguments = json.loads(call.arguments or "{}")
                except json.JSONDecodeError:
                    arguments = {}
                result = self.tool_registry.call(call.name, arguments)
                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": result,
                    }
                )

            response = self._create_response(input_items, tools)

        return "Tool-step limit reached. I stopped safely instead of continuing an uncontrolled action chain."
