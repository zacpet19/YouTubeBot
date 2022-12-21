from gtts import gTTS
from moviepy.editor import AudioFileClip
from moviepy.audio.fx.audio_loop import *
import os 

class TextToSpeech:
    @staticmethod
    def textToSpeech(text):
        if not os.path.exists("./audio"):
            os.makedirs("./audio")
        count = 1
        for i in text:
            stringBuilder = ""
            for j in i:
                stringBuilder += j
            audio = gTTS(text=stringBuilder,lang = "en", slow=False, tld = "US")
            audio.save(f"./audio/{count}.mp3")
            count += 1

    @staticmethod
    def makeAudioFileSameLength(clipPath : str, clipToChangePath : str):
        """This will take in filepaths to two audio files with the first file being the one that will set the lenght
        for the other file. This might need to be run in a try block because it throws a (OSError: [WinError 6] The
        handle is invalid) even if it successfully makes a new mp3 and the reason for this cannot be found at this
        time"""
        clip = AudioFileClip(clipPath)
        clipToChange = AudioFileClip(clipToChangePath)
        if clip.duration < clipToChange.duration:
            clipToChange = clipToChange.subclip(0, clip.duration - 1)
            clipToChange.write_audiofile("modMusic.mp3")
            print("music shortened")
        else:
            #succesfully loops the audio and creates a new file but errors out for some reason
            clipToChange = audio_loop(clipToChange, duration=clip.duration - 1)
            clipToChange.write_audiofile("modMusic.mp3")
            print("musiclooped")





