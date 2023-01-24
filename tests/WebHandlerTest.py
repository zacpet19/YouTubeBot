import sys
import os   
sys.path.append('..')
from dotenv import load_dotenv

from src.webHandler import WebHandler

def invalidPathTest():
    errorThrown = False
    try:
        a = WebHandler("")
        a.screenShotReddit(["https://www.reddit.com/r/csMajors/comments/zn6k7r/recruiter_call_wasted_me_whole_30_mins_and_tells/"])
    except Exception:
        errorThrown = True
    
    assert errorThrown == True
    print("Invalid Path Test Passed")

def invalidUrlTest():
    screenshot = WebHandler("a")
    errorThrown = False
    try:
        screenshot.screenShotReddit(["https://google.com"])
    except Exception:
        errorThrown = True
    assert errorThrown == True
    print("Invalid URL Test Passed")

def screenshotTest():
    screenshot = WebHandler("a")
    screenshot.screenShotReddit(["https://www.reddit.com/r/csMajors/comments/zn6k7r/recruiter_call_wasted_me_whole_30_mins_and_tells/", "https://www.reddit.com/r/csMajors/comments/zn6k7r/recruiter_call_wasted_me_whole_30_mins_and_tells/"])
    assert os.path.exists("./images")
    assert os.path.exists("./images/1.png")
    assert os.path.exists("./images/2.png")
    os.remove("./images/2.png")
    os.remove("./images/1.png")
    os.rmdir("./images")
    print("Screenshot Test Passed")

def uploadVideoTest():
    load_dotenv()

    gmail = os.getenv('gmail')
    password = os.getenv('gmailPassword')
    channel = os.getenv('youtubeChannel')
    videoPath = os.getenv("testFinalVideoPath")
    driverLocation = os.getenv("driver_location")
    videoData = {"Title" : "Test", "Description" : "This is a test upload"}

    web = WebHandler(driverLocation)
    web.uploadYoutubeVideo(channel, gmail, password, videoPath, videoData)

    assert os.path.exists("./test.mp4")
    print("Upload Test Passed")


def uploadVideoWithHeadlessChromeTest():
    load_dotenv()

    gmail = os.getenv('gmail')
    password = os.getenv('gmailPassword')
    channel = os.getenv('youtubeChannel')
    videoPath = os.getenv("testFinalVideoPath")
    driverLocation = os.getenv("driver_location")
    videoData = {"Title" : "Headless Test", "Description" : "This is a headless chrome test upload"}

    web = WebHandler(driverLocation, headless=True)
    web.uploadYoutubeVideo(channel, gmail, password, videoPath, videoData)

    assert os.path.exists("./test.mp4")
    print("Upload Test Passed")


# invalidPathTest()
# invalidUrlTest()
# screenshotTest()
# uploadVideoTest()
uploadVideoWithHeadlessChromeTest()
