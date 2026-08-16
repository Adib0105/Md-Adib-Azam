# JARVIS AI V2 — Created by Adib Azam

A bilingual Hinglish + English Windows desktop AI assistant with an OpenAI-powered agent brain, live web knowledge, hosted Code Interpreter, screen vision, persistent local memory, voice input/output, wake-word mode, read-only local file intelligence, and permission-gated computer control.

> Identity behavior: when asked who created this custom JARVIS assistant, it answers: **“Adib Azam ne mujhe banaya hai.”**

## V2 capabilities

### AI brain
- OpenAI Responses API
- Native multi-step function/tool calling
- Hinglish + English conversation
- Fresh web search when current information is needed
- Hosted Code Interpreter for calculations, Python and data-analysis work
- Up to a configurable number of tool/action rounds per request
- Local conversation context + long-term facts

### Vision
- Takes a screenshot of the current desktop
- Sends the screenshot to the multimodal model only after permission
- Can explain visible UI, errors, pages, buttons and screen content
- Never claims a click happened unless a local action tool actually succeeds

### Voice
- Offline text-to-speech with `pyttsx3`
- Microphone speech input
- One-shot voice command from CLI or GUI
- Wake phrases such as `JARVIS`, `Hey JARVIS`, and `OK JARVIS`

### Windows control
Allowlisted local actions include:
- Open Notepad, Calculator, Paint, Explorer and Task Manager
- Open approved HTTP/HTTPS URLs
- Type text into the active application
- Press keyboard shortcuts
- Click explicit screen coordinates
- Scroll
- Change/mute volume
- Read/write clipboard
- Take screenshots
- Lock the workstation

Interactive or private-data actions are permission-gated. The project deliberately does **not** expose a generic host shell, password/credential extraction, file deletion, software install/uninstall, or security-bypass tool.

### Local memory
- Thread-safe SQLite database
- Conversation history
- Explicit long-term facts/preferences
- Memory search/recall
- `/clear` clears conversation history while keeping long-term facts

### Local file intelligence
JARVIS can, after approval:
- Search file names in approved folders
- Read safe text/code files
- Default roots: Desktop, Documents and Downloads
- Custom roots can be configured with `ALLOWED_FILE_ROOTS`
- Secret-like paths, `.env`, SSH keys, AppData, `.git`, credentials/secrets folders and unsupported binary files are blocked from direct reading
- File tools are read-only; no delete/overwrite tool is provided

## Project structure

```text
jarvis-ai/
├── brain.py             # OpenAI agent brain + multi-step hosted/local tools
├── computer.py          # Allowlisted Windows control layer
├── config.py            # Environment and feature switches
├── desktop_ui.py        # Tkinter GUI + permission popups + voice button
├── listen.py            # Microphone + wake-word listening
├── local_files.py       # Read-only approved-folder file intelligence
├── main.py              # Runtime/orchestrator + CLI + wake-word mode
├── memory.py            # Thread-safe SQLite conversation/fact memory
├── permissions.py       # Central approval policy
├── self_check.py        # Environment/PC readiness check
├── tools.py             # Function-tool schemas and dispatcher
├── vision.py            # Multimodal screenshot understanding
├── voice.py             # Text-to-speech
├── setup_windows.ps1    # Windows setup helper
├── run_jarvis.bat       # Double-click GUI launcher
├── requirements.txt
├── .env.example
└── .gitignore
```

## Windows installation

Open PowerShell inside the `jarvis-ai` folder and run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup_windows.ps1
```

The setup script creates `.venv`, installs dependencies and creates `.env` if it does not already exist.

Then open `.env` and replace:

```text
OPENAI_API_KEY=put_your_api_key_here
```

with your own OpenAI API key. **Never commit the real `.env` file or API key.**

## Check your PC

```powershell
.\.venv\Scripts\python.exe self_check.py
```

Fix any `FAIL` item before relying on voice/computer tools.

## Launch

### Desktop app
Double-click:

```text
run_jarvis.bat
```

or run:

```powershell
.\.venv\Scripts\python.exe desktop_ui.py
```

### Terminal mode

```powershell
.\.venv\Scripts\python.exe main.py
```

CLI commands:
- `/voice` — listen to one microphone command
- `/wake` — stay in wake-word mode
- `/clear` — clear conversation history, keep long-term facts
- `exit` — close JARVIS

## Example prompts

```text
Tumhe kisne banaya?
Latest AI news kya hai?
Python me 100000 rows ka sample analysis karke explain karo.
Mere screen par kya dikh raha hai?
Calculator kholo.
Volume thoda badhao.
Mera clipboard kya hai?
Documents me resume naam ka file dhundo.
Is Python file ko padho aur bug explain karo.
Remember that I prefer Hinglish answers.
Maine pehle kya preference save karwayi thi?
```

## Configuration

`.env` supports:

```text
OPENAI_MODEL=gpt-5.1
JARVIS_NAME=JARVIS
CREATOR_NAME=Adib Azam
USER_NAME=Adib
DEFAULT_LANGUAGE=hinglish
REQUIRE_CONFIRMATION=true
ENABLE_WEB_SEARCH=true
ENABLE_SCREEN_VISION=true
ENABLE_CODE_INTERPRETER=true
MAX_TOOL_STEPS=8
WAKE_WORDS=jarvis,hey jarvis,ok jarvis
ALLOWED_FILE_ROOTS=
```

`ALLOWED_FILE_ROOTS` is optional and uses semicolon-separated Windows paths, for example:

```text
ALLOWED_FILE_ROOTS=C:\Users\Adib\Documents;D:\Projects
```

If blank, JARVIS uses Desktop, Documents and Downloads under the current Windows user profile.

## Permission model

Actions that can affect applications or expose private local data are designed to request approval. Keep `REQUIRE_CONFIRMATION=true` for normal use.

The permission layer is intentional. An AI assistant with unrestricted host-level execution can make mistakes at machine speed. V2 aims for high capability with explicit boundaries and visible authorization.

## Current limitations

- Wake-word recognition currently uses the `SpeechRecognition` microphone stack rather than native OpenAI speech-to-speech Realtime mode.
- Screen vision can understand screenshots, but it is instructed not to guess click coordinates.
- Direct reading is intentionally limited to safe text/code formats; PDF/DOCX/XLSX/PPTX can be found by filename but are not parsed locally in this version.
- PC tools only work while JARVIS is running on the Windows computer.
- OpenAI API usage requires an API key and may incur API costs depending on usage/model/tools.

## Next upgrades

Possible V3 modules:
- Native OpenAI Realtime speech-to-speech
- Better voice activity detection/interruption
- OCR-free document vision for PDFs/images
- User-defined custom skills/plugins
- Calendar/email connectors
- Browser automation with domain-level permissions
- Smart-home/IoT adapters
- Optional local/offline model fallback
- Encrypted memory vault
- Packaging as a signed Windows executable

---

**JARVIS project creator:** Adib Azam
