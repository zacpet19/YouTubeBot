import os

import redditScraper
from TextToSpeech import TextToSpeech
from screenshotWebpage import ScreenShot
from moviepy.editor import AudioFileClip
from Video import VideoMethods
from dotenv import load_dotenv

load_dotenv()
gmail = os.getenv('gmail')
password = os.getenv('gmailPassword')
channel = os.getenv('youtubeChannel')
#this needs an absolute filepath
finalVideoPath = os.getenv('finalVideoPath')

def main():
    (comments, urls) = redditScraper.getTopPostComments("csmajors")
    screenShotter = ScreenShot("a")
    screenShotter.takeScreenShot(urls)
    screenShotter.closeDriver()
    TextToSpeech.textToSpeech(comments)
    randomBackgroundMusic = TextToSpeech.getRandomFile("bndms")
    TextToSpeech.makeAudioFileSameLength("audio/1.mp3", f"bndms/{randomBackgroundMusic}")
    TextToSpeech.mergeAudioFiles(["audio/1.mp3", "audio/modMusic.mp3"])
    finalAudio = AudioFileClip("audio/finalAudio.mp3")
    finalAudioDuration = int(finalAudio.duration)
    finalAudio.close()
    VideoMethods.formatBackgroundVideoForYoutubeShort("video/1.mp4", finalAudioDuration)
    VideoMethods.resizeImageToEvenDimensions("images/1.png")
    VideoMethods.createImageVideo("images/reSizedImage.png", finalAudioDuration)
    VideoMethods.resizeVideoClip("video/imageVideo.mp4", 800, 500)
    VideoMethods.combineVideoClips("video/silentVideo.mp4", "video/resizedVideo.mp4")
    VideoMethods.setVideoClipAudio("video/combinedVideo.mp4", "audio/finalAudio.mp3")
    thisDict = {"Title" : "Reddit Test Video", "Description" : "Test"}
    youtubeUploader = ScreenShot("a")
    youtubeUploader.uploadYoutubeVideo(channel, gmail, password, finalVideoPath, thisDict)
    youtubeUploader.closeDriver()
if __name__ == '__main__':
    main()

