import os
from redditScraper import RedditScraper
from Audio import AudioMethods
from webHandler import WebHandler
from moviepy.editor import AudioFileClip
from Video import VideoMethods
from Logger import Logger
from dotenv import load_dotenv
import sys



def main():
    logger = Logger()
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

    logger.info("Environment Variables loaded")
    #declaring variables to store things found in the while loop
    foundUsableRedditPosts = False
    comments = ""
    urls = ""
    parsedTextToSpeech = ""
    count = 0
    retries = 5
    reddit = RedditScraper(client_id, client_secret, user_agent)
    #loops until it is able to get a usable mp3 file from Reddit posts
    while not foundUsableRedditPosts:
        if count > retries:
            logger.error("Unable to find usable reddit posts, shutting down")
            sys.exit()
        count += 1
        #Scrape reddit posts
        (comments, urls) = reddit.getTopPostAndComments("csmajors")
        commentsForGTTS = []
        for i in comments:
            temp = []
            for j in i:
                temp.append(reddit.ignoreWords(j))
            commentsForGTTS.append(temp)
        logger.info("Potential Reddit posts scraped")

        #Create gTTS .mp3 files with reddit posts
        AudioMethods.removeAudioFolder()
        AudioMethods.textToSpeech(commentsForGTTS, silencePath="permAudio/500milsil.mp3")
        parsedTextToSpeech = AudioMethods.parseTextToSpeechMP3s()
        if len(parsedTextToSpeech) > 0:
            foundUsableRedditPosts = True
        else:
            logger.warn(f"Reddit posts not accepted, retrying {count}/{retries}...")
            
    logger.info("Text to speech sucessfully created, moving on")

    #Take screenshots of reddit posts
    screenShotter = WebHandler("a") #finds the driver no matter the given parameter
    screenShotter.screenShotRedditPosts(urls)
    screenShotter.closeDriver()

    #Pull random audio file from bndms directory and change it's length to match the first TTS file
    randomBackgroundMusic = AudioMethods.getRandomFile("bndms")
    logger.info("Background music used was " + randomBackgroundMusic)
    AudioMethods.changeAudioClipVolume(f"bndms/{randomBackgroundMusic}", "audio/changedVol.mp3", .2)
    AudioMethods.makeAudioFileSameLength(parsedTextToSpeech[0], "audio/changedVol.mp3")
    logger.info("background music created")

    #Merge TTS audio with background music 
    AudioMethods.mergeAudioFiles([parsedTextToSpeech[0], "audio/modMusic.mp3"])
    logger.info("Audio files merged")


    #Get duration of the merged .mp3 file
    finalAudio = AudioFileClip("audio/finalAudio.mp3")
    finalAudioDuration = int(finalAudio.duration)
    finalAudio.close()
    #Pull random video from bndvd directory and format it for youtube shorts
    randomBackgroundVideo = AudioMethods.getRandomFile("bndvd")
    backgroundVideoStart = VideoMethods.getRandomPointInVideo(f"bndvd/{randomBackgroundVideo}")
    VideoMethods.formatBackgroundVideoForYoutubeShort(f"bndvd/{randomBackgroundVideo}", finalAudioDuration,
                                                      startCut=backgroundVideoStart)
    logger.info("Background video formatted")

    #Resize post screenshot to fit youtube shorts
    (imageWidth, _imageHeight) = VideoMethods.resizeImageForYouTubeShort(f"images/{parsedTextToSpeech[0][6:7]}.png")
    logger.info("Image resized")

    # Turns post image into .mp4 file 
    VideoMethods.createImageVideo("images/reSizedImage.png", finalAudioDuration)
    logger.info("Image video created")

    #Merge background video with post video
    #YouTube shorts are 1080 pixels wide
    newYPos = (1080 - imageWidth) / 2
    VideoMethods.combineVideoClips("video/silentVideo.mp4", "video/imageVideo.mp4", xPosition=65, yPosition=newYPos)
    logger.info("Final Video made")

    #Combine merged audio file with merged video file
    VideoMethods.setVideoClipAudio("video/combinedVideo.mp4", "audio/finalAudio.mp3")
    logger.info("Final video given Audio")

    #Pull title and description from comments
    title = comments[int(parsedTextToSpeech[0][6:7]) - 1][0]
    if len(title) > 50:
        title = f"{title[:50]}..."
    description = comments[int(parsedTextToSpeech[0][6:7]) - 1][0]
    videoData = {"Title" : title, "Description" : description}

    #Upload video to youtube
    youtubeUploader = WebHandler("a") #finds the driver no matter the given string
    youtubeUploader.uploadYoutubeVideo(channel, gmail, password, finalVideoPath, videoData)
    youtubeUploader.closeDriver()
    logger.info("Video uploaded")


if __name__ == '__main__':
    main()

