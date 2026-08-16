import speech_recognition as sr

from config import WAKE_WORDS


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True

    def listen_once(self, language="en-IN", timeout=8, phrase_time_limit=25):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.35)
            audio = self.recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )
        return self.recognizer.recognize_google(audio, language=language).strip()

    def wait_for_wake_word(self, language="en-IN"):
        """Listen until a configured wake phrase is heard.

        Returns any command spoken after the wake phrase, or an empty string if
        the user only said the wake phrase.
        """
        while True:
            try:
                text = self.listen_once(language=language, timeout=None, phrase_time_limit=12)
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                continue
            lowered = text.lower()
            for wake in WAKE_WORDS:
                pos = lowered.find(wake)
                if pos >= 0:
                    return text[pos + len(wake):].strip(" ,.-")
