import time

import numpy as np
import sounddevice as sd
import speech_recognition as sr

from config import WAKE_WORDS


class Listener:
    SAMPLE_RATE = 16000
    CHANNELS = 1
    SAMPLE_WIDTH = 2  # int16
    BLOCK_SECONDS = 0.10
    SILENCE_AFTER_SPEECH = 1.0

    def __init__(self):
        self.recognizer = sr.Recognizer()

    @staticmethod
    def _rms(block) -> float:
        if block is None or len(block) == 0:
            return 0.0
        data = block.astype(np.float32)
        return float(np.sqrt(np.mean(np.square(data))))

    def listen_once(self, language="en-IN", timeout=8, phrase_time_limit=25):
        """Record one spoken command without requiring PyAudio.

        Uses sounddevice/PortAudio directly so Windows + Python 3.14 can use
        microphone input without compiling PyAudio from source.
        """
        blocksize = int(self.SAMPLE_RATE * self.BLOCK_SECONDS)
        calibration_blocks = 4
        frames = []
        speech_started = False
        silence_for = 0.0
        started_at = time.monotonic()
        speech_started_at = None

        try:
            with sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=self.CHANNELS,
                dtype="int16",
                blocksize=blocksize,
            ) as stream:
                ambient_levels = []
                for _ in range(calibration_blocks):
                    block, _overflowed = stream.read(blocksize)
                    ambient_levels.append(self._rms(block))

                ambient = float(np.median(ambient_levels)) if ambient_levels else 0.0
                threshold = max(250.0, ambient * 3.0)

                while True:
                    block, _overflowed = stream.read(blocksize)
                    level = self._rms(block)
                    now = time.monotonic()

                    if not speech_started:
                        if level >= threshold:
                            speech_started = True
                            speech_started_at = now
                            frames.append(block.copy())
                        elif timeout is not None and (now - started_at) >= timeout:
                            raise sr.WaitTimeoutError("Listening timed out while waiting for speech")
                        continue

                    frames.append(block.copy())

                    if level >= threshold:
                        silence_for = 0.0
                    else:
                        silence_for += self.BLOCK_SECONDS

                    if silence_for >= self.SILENCE_AFTER_SPEECH:
                        break

                    if phrase_time_limit is not None and speech_started_at is not None:
                        if (now - speech_started_at) >= phrase_time_limit:
                            break

        except sr.WaitTimeoutError:
            raise
        except Exception as exc:
            raise RuntimeError(f"Microphone capture failed: {exc}") from exc

        if not frames:
            raise sr.UnknownValueError()

        pcm = np.concatenate(frames, axis=0).reshape(-1).astype(np.int16).tobytes()
        audio = sr.AudioData(pcm, self.SAMPLE_RATE, self.SAMPLE_WIDTH)
        return self.recognizer.recognize_google(audio, language=language).strip()

    def wait_for_wake_word(self, language="en-IN"):
        """Listen until a configured wake phrase is heard."""
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
