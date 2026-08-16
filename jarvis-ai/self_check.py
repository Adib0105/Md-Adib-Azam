import os
import platform

from config import ALLOWED_FILE_ROOTS, ENABLE_SCREEN_VISION, ENABLE_WEB_SEARCH, OPENAI_API_KEY, OPENAI_MODEL


def check(label, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail else ""))
    return bool(ok)


def main():
    results = []
    results.append(check("Python", tuple(map(int, platform.python_version_tuple()[:2])) >= (3, 10), platform.python_version()))
    results.append(check("Operating system", os.name == "nt", platform.platform()))
    results.append(check("OpenAI API key configured", bool(OPENAI_API_KEY), "Set OPENAI_API_KEY in .env" if not OPENAI_API_KEY else "configured"))
    results.append(check("OpenAI model", bool(OPENAI_MODEL), OPENAI_MODEL))
    results.append(check("Web search setting", True, f"enabled={ENABLE_WEB_SEARCH}"))
    results.append(check("Screen vision setting", True, f"enabled={ENABLE_SCREEN_VISION}"))

    existing_roots = [str(p) for p in ALLOWED_FILE_ROOTS if p.exists()]
    results.append(check("At least one local-file root exists", bool(existing_roots), "; ".join(existing_roots) or "none"))

    try:
        import pyautogui
        size = pyautogui.size()
        results.append(check("Desktop automation", True, f"screen={size.width}x{size.height}"))
    except Exception as exc:
        results.append(check("Desktop automation", False, str(exc)))

    try:
        import speech_recognition as sr
        microphones = sr.Microphone.list_microphone_names()
        results.append(check("Microphone detection", bool(microphones), f"{len(microphones)} device(s)"))
    except Exception as exc:
        results.append(check("Microphone detection", False, str(exc)))

    print("\nJARVIS self-check:", "READY" if all(results) else "NEEDS ATTENTION")
    if not all(results):
        print("Fix the FAIL items above, then run: python self_check.py")


if __name__ == "__main__":
    main()
