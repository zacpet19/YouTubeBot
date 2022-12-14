import sys
import os   
sys.path.append('..')

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

invalidPathTest()
invalidUrlTest()
screenshotTest()