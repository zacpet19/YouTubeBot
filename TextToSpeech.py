from gtts import gTTS
from moviepy.editor import AudioFileClip
from moviepy.audio.fx.audio_loop import *
from moviepy.editor import CompositeAudioClip
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
        """This will take in filepaths to two audio files with the first file being the one that will set the length
        for the other file."""
        if not os.path.exists("./audio"):
            os.makedirs("./audio")
        clip = AudioFileClip(clipPath)
        clipToChange = AudioFileClip(clipToChangePath)
        if clip.duration < clipToChange.duration:
            clipToChangeSubclip = clipToChange.subclip(0, clip.duration - 1)
            clipToChangeSubclip.write_audiofile("audio/modMusic.mp3")
            clipToChangeSubclip.close()
        else:
            clipToChangeLooped = audio_loop(clipToChange, duration=clip.duration - 1)
            clipToChangeLooped.write_audiofile("audio/modMusic.mp3")
            clipToChangeLooped.close()
        clip.close()
        clipToChange.close()

    @staticmethod
    def mergeAudioFiles(clipsToMerge : list):
        """Takes in a list of audio clip objects and then merges them all together and saves the new clip into memory.
        They will all start at the same time so if they vary in length the longest one will continue to play to
         completion after the others have stopped"""
        if not os.path.exists("./audio"):
            os.makedirs("./audio")
        mergedAudio = CompositeAudioClip(clipsToMerge)
        mergedAudio.write_audiofile("audio/finalAudio.mp3", fps=44100)
        mergedAudio.close()



