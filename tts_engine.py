import pyttsx3
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.rate = self.engine.getProperty('rate')
        self.volume = self.engine.getProperty('volume')

    def set_voice(self, voice_id):
        self.engine.setProperty('voice', voice_id)

    def set_rate(self, rate):
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        self.engine.setProperty('volume', volume)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def save_audio(self, text, filename, language='en'):
        tts = gTTS(text=text, lang=language)
        tts.save(filename)

    def play_audio(self, filename):
        audio = AudioSegment.from_file(filename)
        play(audio)
