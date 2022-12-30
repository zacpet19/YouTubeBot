import os
from redditScraper import RedditScraper
from TextToSpeech import TextToSpeech
from screenshotWebpage import ScreenShot
from moviepy.editor import AudioFileClip
from Video import VideoMethods
from dotenv import load_dotenv



def main():

    load_dotenv()
    gmail = os.getenv('gmail')
    password = os.getenv('gmailPassword')
    channel = os.getenv('youtubeChannel')
    #this needs an absolute filepath
    finalVideoPath = os.getenv('finalVideoPath')
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    user_agent = os.getenv('user_agent')

    TextToSpeech.removeAudioFolder()
    reddit = RedditScraper(client_id,client_secret,user_agent)
    (comments, urls) = reddit.getTopPostComments("askreddit")
    screenShotter = ScreenShot("a")
    screenShotter.takeScreenShot(urls)
    print("Reddit Scraped")
    screenShotter.closeDriver()
    TextToSpeech.textToSpeech(comments, silencePath="permAudio/500milsil.mp3")
    print("text to speech complete")
    parsedTextToSpeech = TextToSpeech.parseTextToSpeechMP3s()
    print(parsedTextToSpeech[0])
    randomBackgroundMusic = TextToSpeech.getRandomFile("bndms")
    TextToSpeech.changeAudioClipVolume(f"bndms/{randomBackgroundMusic}", "audio/changedVol.mp3", .2)
    TextToSpeech.makeAudioFileSameLength(parsedTextToSpeech[0], "audio/changedVol.mp3")
    print("random background music created")
    TextToSpeech.mergeAudioFiles([parsedTextToSpeech[0], "audio/modMusic.mp3"])
    print("Audio files merged")
    finalAudio = AudioFileClip("audio/finalAudio.mp3")
    finalAudioDuration = int(finalAudio.duration)
    finalAudio.close()
    randomBackgroundVideo = TextToSpeech.getRandomFile("bndvd")
    VideoMethods.formatBackgroundVideoForYoutubeShort(f"bndvd/{randomBackgroundVideo}", finalAudioDuration)
    print("Background video formatted")
    (imageWidth, _imageHeight) = VideoMethods.resizeImageForYouTubeShort(f"images/{parsedTextToSpeech[0][6:7]}.png")
    print("Image resized")
    VideoMethods.createImageVideo("images/reSizedImage.png", finalAudioDuration)
    print("Image video created")
    #YouTube shorts are 1080 pixels wide
    newYPos = (1080 - imageWidth) / 2
    VideoMethods.combineVideoClips("video/silentVideo.mp4", "video/imageVideo.mp4", xPosition=65, yPosition=newYPos)
    print("Final Video made")
    VideoMethods.setVideoClipAudio("video/combinedVideo.mp4", "audio/finalAudio.mp3")
    print("Final video given Audio")
    #parsed textToSpeech contains the relative filepath names of the textToSpeech files. Since they are named
    #numerically this slice will be the number given to it
    title = comments[int(parsedTextToSpeech[0][6:7]) - 1][0]
    if len(title) > 50:
        title = f"{title[:50]}..."
    description = comments[int(parsedTextToSpeech[0][6:7]) - 1][0]
    videoData = {"Title" : title, "Description" : description}
    youtubeUploader = ScreenShot("a")
    youtubeUploader.uploadYoutubeVideo(channel, gmail, password, finalVideoPath, videoData)
    print("Video uploaded")
    youtubeUploader.closeDriver()
if __name__ == '__main__':
    main()

