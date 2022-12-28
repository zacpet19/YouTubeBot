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
    print("Reddit Scraped")
    screenShotter.closeDriver()
    TextToSpeech.textToSpeech(comments)
    print("text to speech complete")
    randomBackgroundMusic = TextToSpeech.getRandomFile("bndms")
    TextToSpeech.changeAudioClipVolume(f"bndms/{randomBackgroundMusic}", "audio/changedVol.mp3", .1)
    TextToSpeech.makeAudioFileSameLength("audio/1.mp3", "audio/changedVol.mp3")
    print("random background music created")
    #need to open mp3 files inside the method
    TextToSpeech.mergeAudioFiles(["audio/1.mp3", "audio/modMusic.mp3"])
    print("Audio files merged")
    finalAudio = AudioFileClip("audio/finalAudio.mp3")
    finalAudioDuration = int(finalAudio.duration)
    finalAudio.close()
    VideoMethods.formatBackgroundVideoForYoutubeShort("video/q.mp4", finalAudioDuration)
    print("Background video formated")
    VideoMethods.resizeImageToEvenDimensions("images/1.png")
    print("Image resized")
    VideoMethods.createImageVideo("images/reSizedImage.png", finalAudioDuration)
    print("Image video created")
    VideoMethods.resizeVideoClip("video/imageVideo.mp4", 600, 800)
    print("Image Video Resized")
    VideoMethods.combineVideoClips("video/silentVideo.mp4", "video/resizedVideo.mp4")
    print("Final Video made")
    VideoMethods.setVideoClipAudio("video/combinedVideo.mp4", "audio/finalAudio.mp3")
    print("Final video given Audio")
    thisDict = {"Title" : "Reddit Test Video", "Description" : "Test"}
    youtubeUploader = ScreenShot("a")
    youtubeUploader.uploadYoutubeVideo(channel, gmail, password, finalVideoPath, thisDict)
    print("Video uploaded")
    youtubeUploader.closeDriver()
if __name__ == '__main__':
    main()

