from gtts import gTTS
from moviepy.editor import AudioFileClip
from moviepy.audio.fx.audio_loop import *
from moviepy.editor import CompositeAudioClip
import os
import random

class TextToSpeech:
    @staticmethod
    def textToSpeech(text):
        """Takes in a 2d array of text and uses gTTP to turn it into a mp3 file and then saves it into memory."""
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
        for the other file. If the first file is shorter it will cut the clip to be change to that size and if the first
        file is longer it will loop the clip to change until it is the same length.Returns false if files cannot be
        found."""
        if not os.path.exists("./audio"):
            os.makedirs("./audio")
        try:
            clip = AudioFileClip(clipPath)
            clipToChange = AudioFileClip(clipToChangePath)
        except Exception as e:
            print("Error: Failed to find one or more of provided files.")
            return False
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
        if len(clipsToMerge) > 1:
            print("Error: List size must be greater that one.")
        try:
            mergedAudio = CompositeAudioClip(clipsToMerge)
        except Exception as e:
            print("Error: Failed to find one or more provided files.")
            return False
        mergedAudio.write_audiofile("audio/finalAudio.mp3", fps=44100)
        mergedAudio.close()

    @staticmethod
    def randomAudioCutout(clipToCutPath : str, duration : int):
        """This method takes in a filepath to and mp3 and a duration you want the new clip to be. Then it randomly
        creates a subclip of the provided duration and then saves it into memory. It will return false if given
        bad parameters."""
        if not os.path.exists("./audio"):
            os.makedirs("./audio")
        if duration == 0:
            print("Error: Duration must be longer than 0")
            return False
        try:
            clip = AudioFileClip(clipToCutPath)
            clipDuration = int(clip.duration)
        except Exception as e:
            print("Error: Failed to find one or more of provided filepaths.")
            return False
        if duration >= clipDuration:
            clip.close()
            print("Error: Duration given longer than audio file length")
            return False
        cut = random.randrange(duration, clipDuration + 1)
        cutAudio = clip.subclip(cut - duration, cut)
        cutAudio.write_audiofile("audio/cutoutAudio.mp3")
        cutAudio.close()
        clip.close()

    @staticmethod
    def getRandomFile(directory : str) -> str:
        """Returns the name of a random file from a given directory. Returns an empty string on failure."""
        try:
            files = os.listdir(directory)
        except Exception as e:
            print("Error: Failed to find directory.")
            return ""
        if len(files) == 0:
            print("Error: Directory has no files.")
            return ""
        randomNum = random.randrange(0, len(files))
        return files[randomNum]






