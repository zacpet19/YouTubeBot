import os
from redditScraper import RedditScraper
from TextToSpeech import TextToSpeech
from screenshotWebpage import ScreenShot
from moviepy.editor import AudioFileClip
from Video import VideoMethods
from dotenv import load_dotenv
import sys



def main():
    # load environment variables
    load_dotenv()
    gmail = os.getenv('gmail')
    password = os.getenv('gmailPassword')
    channel = os.getenv('youtubeChannel')
    #this needs an absolute filepath
    finalVideoPath = os.getenv('finalVideoPath')
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    user_agent = os.getenv('user_agent')
    #Should check for missing environment variables here

    #declaring variables to store things found in the while loop
    foundUsableRedditPosts = False
    comments = ""
    urls = ""
    parsedTextToSpeech = ""
    count = 0
    reddit = RedditScraper(client_id, client_secret, user_agent)
    #loops until it is able to get a usable mp3 file from Reddit posts
    while not foundUsableRedditPosts:
        if count > 20:
            print("Error: Unable to find usable reddit posts.")
            sys.exit()
        count += 1
        #Scrape reddit posts
        (comments, urls) = reddit.getTopPostComments("csmajors")
        print("Reddit Scraped")

        #Create TTS .mp3 files with reddit posts
        TextToSpeech.removeAudioFolder()
        TextToSpeech.textToSpeech(comments, silencePath="permAudio/500milsil.mp3")
        parsedTextToSpeech = TextToSpeech.parseTextToSpeechMP3s()
        if len(parsedTextToSpeech) > 0:
            foundUsableRedditPosts = True
            
    print("text to speech complete")

    #Take screenshots of reddit posts
    screenShotter = ScreenShot("a")
    screenShotter.takeScreenShot(urls)
    screenShotter.closeDriver()

    #Pull random audio file from bndms directory and change it's length to match the first TTS file
    randomBackgroundMusic = TextToSpeech.getRandomFile("bndms")
    TextToSpeech.changeAudioClipVolume(f"bndms/{randomBackgroundMusic}", "audio/changedVol.mp3", .2)
    TextToSpeech.makeAudioFileSameLength(parsedTextToSpeech[0], "audio/changedVol.mp3")
    print("random background music created")

    #Merge TTS audio with background music 
    TextToSpeech.mergeAudioFiles([parsedTextToSpeech[0], "audio/modMusic.mp3"])
    print("Audio files merged")


    #Get duration of the merged .mp3 file
    finalAudio = AudioFileClip("audio/finalAudio.mp3")
    finalAudioDuration = int(finalAudio.duration)
    finalAudio.close()
    #Pull random video from bndvd directory and format it for youtube shorts
    randomBackgroundVideo = TextToSpeech.getRandomFile("bndvd")
    VideoMethods.formatBackgroundVideoForYoutubeShort(f"bndvd/{randomBackgroundVideo}", finalAudioDuration)
    print("Background video formatted")

    #Resize post screenshot to fit youtube shorts
    (imageWidth, _imageHeight) = VideoMethods.resizeImageForYouTubeShort(f"images/{parsedTextToSpeech[0][6:7]}.png")
    print("Image resized")

    # Turns post image into .mp4 file 
    VideoMethods.createImageVideo("images/reSizedImage.png", finalAudioDuration)
    print("Image video created")

    #Merge background video with post video
    #YouTube shorts are 1080 pixels wide
    newYPos = (1080 - imageWidth) / 2
    VideoMethods.combineVideoClips("video/silentVideo.mp4", "video/imageVideo.mp4", xPosition=65, yPosition=newYPos)
    print("Final Video made")

    #Combine merged audio file with merged video file
    VideoMethods.setVideoClipAudio("video/combinedVideo.mp4", "audio/finalAudio.mp3")
    print("Final video given Audio")

    #Pull title and description from comments
    title = comments[int(parsedTextToSpeech[0][6:7]) - 1][0]
    if len(title) > 50:
        title = f"{title[:50]}..."
    description = comments[int(parsedTextToSpeech[0][6:7]) - 1][0]
    videoData = {"Title" : title, "Description" : description}

    #Upload video to youtube
    youtubeUploader = ScreenShot("a")
    youtubeUploader.uploadYoutubeVideo(channel, gmail, password, finalVideoPath, videoData)
    youtubeUploader.closeDriver()
    print("Video uploaded")


if __name__ == '__main__':
    main()

