from gtts import gTTS
from moviepy.editor import AudioFileClip
from moviepy.editor import concatenate_audioclips
from moviepy.audio.fx.audio_loop import *
from moviepy.audio.fx.volumex import *
from moviepy.editor import CompositeAudioClip
import os
import random
import shutil


"""Current known Audio issues: Text to speech says random punctuation and says things you cant see like if there is a 
whole bunch of spaces(ie. hashx200b was said multiple times in one. at the end of some videos there is a "brrt" sound"""

class AudioMethods:
    """AudioMethods class is methods for general audio file manipulation/creation for use in YouTube videos."""
    @staticmethod
    def textToSpeech(text, silencePath=""):
        """Takes in a 2d array of text (reddit post/comments and uses gTTP to turn it into a mp3 file and then saves it
        into memory while keeping it under a minute long. The silence path is a variable that takes in the file path to
        a silence audioClip if you would like to have pauses between comments and posts. You could add any other mp3
        files between them as well. Returns an array of the number of comments used to make each mp3. The order of the
         returned array is in the same order the posts were given."""
        if not os.path.exists("./audio"):
            os.makedirs("./audio")
        count = 1
        #this is to help account for added audio duration from a silent clip or anything else in between posts/comments
        inBetweenAudioDuration = 0
        if silencePath != "":
            try:
                inBetweenAudio = AudioFileClip(silencePath)
            except Exception as e:
                print("Error: Failed to find provided audio path")
                raise e
            inBetweenAudioDuration = inBetweenAudio.duration
            inBetweenAudio.close()
        #TODO: make list again if needed
        commentsUsed = 0
        #list of durations(floats) for each comment mp4 made
        #TODO: might need to be a 2d array of floats
        mp4Durations = []
        postBody = True
        for i in text:
            if not os.path.exists(f"./audio/post{count}"):
                os.makedirs(f"./audio/post{count}")
            duration = 0
            innerCount = 1
            for j in i:
                #reddit scraper will pull empty string if the post body is empty and this is to address that
                if j == "":
                    if innerCount == 2:
                        postBody = False
                    continue
                #creating individual audio clips
                audio = gTTS(text=j,lang = "en", slow=False, tld = "US")
                audio.save(f"./audio/post{count}/{innerCount}.mp3")
                audioToAdd = AudioFileClip(f"./audio/post{count}/{innerCount}.mp3")
                duration += audioToAdd.duration
                audioToAdd.close()
                if duration >= 60:
                    break
                duration += inBetweenAudioDuration
                innerCount += 1
            #wont create final clip if only title audio clips was made
            if innerCount > 2:
                audioFilePaths = os.listdir(f"./audio/post{count}")
                #removes last audio file created because it would make the clip go over 60 seconds
                if duration >= 60:
                    audioFilePaths.pop()
                #subtracts 2 to account for post title and body
                commentsUsed = (len(audioFilePaths) - 2)
                clips = []
                for c in audioFilePaths:
                    clips.append(AudioFileClip(f"./audio/post{count}/{c}"))
                    mp4Durations.append(clips[-1].duration)
                    #adds the audio clip you want played in between comments/posts
                    if silencePath != "" and c != audioFilePaths[-1]:
                        clips.append(AudioFileClip(silencePath))
                finalClip = concatenate_audioclips(clips)
                finalClip.write_audiofile(f"audio/{count}.mp3")
                for clip in clips:
                    clip.close()
            else:
                print("Initial text body provided was too long or only post title audio was included")
            #Be careful messing with this because it removes an entire directory and all things below it
            shutil.rmtree(f"audio/post{count}")
            count += 1
        #returns an int and a list of floats
        return (commentsUsed, mp4Durations, postBody)

    @staticmethod
    def parseTextToSpeechMP3s():
        """Parses the text to speech mp3 files by making sure they are not too short to long. Returns a list of the
        file names that match the given criteria. Notably will return an empty list if no suitable files are found."""
        if not os.path.exists("./audio"):
            return []
        count = 1
        textToSpeechFileNames = []
        while count < 6:
            if os.path.exists(f"audio/{count}.mp3"):
                clip = AudioFileClip(f"audio/{count}.mp3")
                if 20 < clip.duration < 60:
                    textToSpeechFileNames.append(f"audio/{count}.mp3")
                clip.close()
            count += 1
        return textToSpeechFileNames

    @staticmethod
    def removeAudioFolder():
        """Removes the audio folder and all subdirectories. Does nothing if audio folder doesn't exist. Many methods of
        this class will create a folder named audio in the CWD."""
        if os.path.exists("./audio"):
            #Be careful messing around with this as it removes entire directories
            shutil.rmtree("audio")

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
        #the audio being changed is looped if it is not longer than the other clip
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
        if len(clipsToMerge) <= 1:
            print("Error: List size must be greater that one.")
            return False
        audioFiles = []
        try:
            for clip in clipsToMerge:
                audioFiles.append(AudioFileClip(clip))
        except Exception as e:
            print("Error: Failed to find one or more provided files.")
            raise e
        mergedAudio = CompositeAudioClip(audioFiles)
        mergedAudio.write_audiofile("audio/finalAudio.mp3", fps=44100)
        mergedAudio.close()
        for file in audioFiles:
            file.close()

    @staticmethod
    def randomAudioCutout(clipToCutPath : str, duration : int):
        """This method takes in a filepath to and mp3 and a duration you want the new clip to be. Then it randomly
        creates a subclip of the provided duration and then saves it into memory. It will return false if given
        unusable parameters."""
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

    @staticmethod
    def changeAudioClipVolume(clipToChange : str, newFileName : str, volume):
        """Uses moviepy to create a new clip with a new volume. Unsure at this time how different number exactly impact
        audio but any volume lower than 1 lowers the volume and anything above 1 should raise the volume. The
        parameter clipToChange should be a file path to a audio file and volume can be an int or a double."""
        if volume <= 0:
            print("New Volume must be larger than 0")
            return False
        try:
            newClip = AudioFileClip(clipToChange)
        except Exception as e:
            print("Error: Failed to find one or more of provided filepaths.")
            return False
        change = volumex(newClip, volume)
        change.write_audiofile(newFileName)
        newClip.close()
        change.close()







