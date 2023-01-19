import os
from src.redditScraper import RedditScraper
from src.Audio import AudioMethods
from src.webHandler import WebHandler
from moviepy.editor import AudioFileClip
from src.Video import VideoMethods
from src.Logger import Logger
from dotenv import load_dotenv
import sys
import random



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
    logger.info("**************** NEW VIDEO CREATION START ****************")
    logger.info("Environment Variables loaded")

    VideoMethods.deleteImageVideoFolder()
    #declaring variables to store things found in the while loop
    foundUsableRedditPosts = False
    comments = ""
    urls = ""
    commentIdsPulled = ""
    numberOfCommentsUsed = 0
    #audioLengths will be a list of floats given by the length of each TTS portion of audio used
    audioLengths = ""
    parsedTextToSpeech = ""
    #determines if the post used has a body or not
    postBody = True
    count = 0
    retries = 5
    reddit = RedditScraper(client_id, client_secret, user_agent)
    # getting random subreddit from list
    subreddits = reddit.subredditList()
    randomSubreddit = subreddits[random.randint(0, len(subreddits) - 1)]
    #loops until it is able to get a usable mp3 file from Reddit posts
    while not foundUsableRedditPosts:
        if count > retries:
            logger.error("Unable to find usable reddit posts, shutting down")
            sys.exit()
        count += 1
        #Scrape reddit posts
        (comments, urls, commentIdsPulled) = reddit.getTopPostAndComments(randomSubreddit)
        logger.info("Potential Reddit posts scraped")

        #Create gTTS .mp3 files with reddit posts
        AudioMethods.removeAudioFolder()
        (numberOfCommentsUsed, audioLengths, postBody) = AudioMethods.textToSpeech(comments,
                                                                                   silencePath="permAudio/500milsil.mp3")
        parsedTextToSpeech = AudioMethods.parseTextToSpeechMP3s()
        if len(parsedTextToSpeech) > 0:
            foundUsableRedditPosts = True
        else:
            logger.warn(f"Reddit posts not accepted, retrying {count}/{retries}...")

    logger.info("Text to speech sucessfully created, moving on")

    #gets the comment ids only of the comments that are used to make the mp3
    commentIdsUsed = commentIdsPulled[:numberOfCommentsUsed]

    #Take screenshots of reddit posts
    screenShotter = WebHandler("a") #finds the driver no matter the given string
    screenShotter.screenShotReddit(urls, commentIds=commentIdsUsed)

    #Pull random audio file from bndms directory and change it's length to match the first TTS file
    randomBackgroundMusic = AudioMethods.getRandomFile("bndms")

    AudioMethods.changeAudioClipVolume(f"bndms/{randomBackgroundMusic}", "audio/changedVol.mp3", .2)
    AudioMethods.makeAudioFileSameLength(parsedTextToSpeech[0], "audio/changedVol.mp3")
    logger.info("background music created")

    #Merge TTS audio with background music 
    AudioMethods.mergeAudioFiles([parsedTextToSpeech[0], "audio/modMusic.mp3"])
    logger.info("Audio files merged")

    #Get duration of the merged .mp3 file
    finalAudio = AudioFileClip("audio/finalAudio.mp3")
    #TODO: Test if int casting this number could be whats causing audio issues
    finalAudioDuration = int(finalAudio.duration)
    finalAudio.close()
    #Pull random video from bndvd directory and format it for youtube shorts
    randomBackgroundVideo = AudioMethods.getRandomFile("bndvd")
    backgroundVideoStart = VideoMethods.getRandomPointInVideo(f"bndvd/{randomBackgroundVideo}")
    VideoMethods.formatBackgroundVideoForYoutubeShort(f"bndvd/{randomBackgroundVideo}", finalAudioDuration,
                                                      startCut=backgroundVideoStart)
    logger.info("Background video formatted")

    #Resize post screenshot(s) to fit youtube shorts
    #list of resized image widths
    imageWidths = []

    #Grabs filenumber from string
    fileNumber = int(parsedTextToSpeech[0][6:7])
    #resizing main post images
    (imageWidth, _imageHeight) = VideoMethods.resizeImageForYouTubeShort(f"images/{fileNumber}.png")
    imageWidths.append(imageWidth)
    #list of relative filepaths to the images being turned into videos
    imagePaths = [f"images/{fileNumber}.png"]

    for count in range(1,numberOfCommentsUsed + 1):
        imagePaths.append(f"images/comment{count}.png")
        (imageWidth, _imageHeight) = VideoMethods.resizeImageForYouTubeShort(imagePaths[count])
        imageWidths.append(imageWidth)

    logger.info("Images resized")

    # Turns post image into .mp4 file
    #startTimes is a list of the durations of the image videos
    startTimes = VideoMethods.createImageVideo(imagePaths, audioLengths, finalAudioDuration=finalAudioDuration,
                                  silencePath="permAudio/500milsil.mp3", postBody=postBody)
    logger.info("Image video created")

    #Merge background video with post video
    #Finds correct yPositions for the images in the video
    count = 0
    for width in imageWidths:
        # YouTube shorts are 1080 pixels wide
        imageWidths[count] = (1080 - width) / 2
        count += 1
    imageVideos = os.listdir("./video/imageVideo")
    count = 0
    for video in imageVideos:
        imageVideos[count] = f"video/imageVideo/{video}"
        count += 1
    imageVideos.insert(0, "video/silentVideo.mp4")
    VideoMethods.combineVideoClips(imageVideos, xPosition=65, yPosition=imageWidths,
                                   startTimes=startTimes)
    logger.info("Final Video made")

    #Combine merged audio file with merged video file
    VideoMethods.setVideoClipAudio("video/combinedVideo.mp4", "audio/finalAudio.mp3")
    logger.info("Final video given Audio")

    #Pull title and description from comments
    title = comments[fileNumber - 1][0]
    if len(title) > 50:
        title = f"{title[:50]}..."
    description = f"{comments[fileNumber - 1][0]}\n\n To make videos like this check out my gitgub at " \
                  f"github.com/zacpet19/YouTubeBot"
    videoData = {"Title" : title, "Description" : description}

    #Upload video to youtube
    screenShotter.uploadYoutubeVideo(channel, gmail, password, finalVideoPath, videoData)
    logger.info("Video uploaded")
    logger.info(f"Video Name: {title}")
    logger.info("Background music used: " + randomBackgroundMusic)
    logger.info("Background video used " + randomBackgroundVideo)


if __name__ == '__main__':
    main()

