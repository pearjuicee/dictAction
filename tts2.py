import os
import playsound
from gtts import gTTS
from pydub import AudioSegment

def speak_slow(text):
    tts = gTTS(text=text, lang="en", slow= True)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def speak_fast(text):
    tts = gTTS(text=text, lang="en", slow=False)
    temp_file = "temp_voice.mp3"
    tts.save(temp_file)

    audio = AudioSegment.from_file(temp_file, format="mp3")
    audio = audio.speedup(playback_speed=1.5) # speed up by 3x

    # export to mp3
    audio.export("final.mp3", format="mp3")
    
    playsound.playsound("final.mp3")

def speak_normal(text):
    tts = gTTS(text=text, lang="en", slow= False)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
