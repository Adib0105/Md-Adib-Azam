# JARVIS AI — Created by Adib Azam

An advanced bilingual Hinglish + English desktop AI assistant with an OpenAI-powered brain, persistent SQLite memory, voice output, microphone input module, desktop GUI, and permission-gated Windows computer control.

## Features

- OpenAI Responses API powered reasoning and Q&A
- Hinglish + English conversation
- Fixed creator identity: `Adib Azam ne mujhe banaya hai.`
- Persistent local SQLite memory
- Offline text-to-speech voice output
- Microphone speech-recognition module
- Desktop Tkinter chat interface
- Safe Windows computer actions: open allowlisted apps, type text, hotkeys, screenshots, lock PC
- Confirmation gate before higher-impact desktop actions
- Modular architecture for adding vision, browser tools, custom skills, APIs, smart-home control, and more

## Project structure

```text
jarvis-ai/
├── brain.py        # AI brain + action planner
├── computer.py     # Windows control layer
├── config.py       # Environment/configuration
├── desktop_ui.py   # Desktop GUI
├── listen.py       # Microphone speech input
├── main.py         # Runtime/orchestrator
├── memory.py       # Persistent SQLite memory
├── voice.py        # Text-to-speech
├── requirements.txt
├── .env.example
└── .gitignore
```

## Windows setup

```powershell
cd jarvis-ai
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and replace `put_your_api_key_here` with your OpenAI API key. Never commit the `.env` file.

## Run terminal JARVIS

```powershell
python main.py
```

## Run desktop JARVIS

```powershell
python desktop_ui.py
```

## Example prompts

- `Tumhe kisne banaya?`
- `Explain machine learning in Hinglish.`
- `Notepad kholo.`
- `Mera system kis OS par chal raha hai?`
- `Screenshot lo.`
- `Python me weather app ka architecture banao.`

## Safety model

JARVIS can control selected parts of the computer, but computer access is deliberately permission-gated. Typing, hotkeys, locking the PC and future sensitive actions should require confirmation. Do not remove approval checks for destructive, financial, credential, privacy-sensitive, delete, install/uninstall, send/post, or system-changing actions.

## Expansion roadmap

1. Wake word: `Hey JARVIS`
2. Streaming speech-to-speech conversation
3. Camera/screen vision
4. Browser automation with domain permissions
5. Calendar/email integrations
6. Local file semantic search
7. Plugin/skill registry
8. Multi-agent planner + executor + verifier
9. Smart-home/IoT integration
10. Optional local/offline LLM fallback

---

**Creator:** Adib Azam
