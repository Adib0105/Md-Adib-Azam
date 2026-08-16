import speech_recognition as sr

class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_once(self, language="en-IN"):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
            audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=20)
        return self.recognizer.recognize_google(audio, language=language)
