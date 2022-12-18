import sys
import os   
sys.path.append('..')

from screenshotWebpage import ScreenShot

def invalidPathTest():
    errorThrown = False
    try:
        ScreenShot("")
    except Exception:
        errorThrown = True
    
    assert errorThrown == True
    print("Invalid Path Test Passed")

def invalidUrlTest():
    screenshot = ScreenShot("")
    errorThrown = False
    try:
        screenshot.takeScreenShot("https://google.com")
    except Exception:
        errorThrown = True
    assert errorThrown == True
    print("Invalid URL Test Passed")

def screenshotTest():
    screenshot = ScreenShot("")
    screenshot.takeScreenShot("https://www.reddit.com/r/csMajors/comments/zn6k7r/recruiter_call_wasted_me_whole_30_mins_and_tells/")
    assert os.path.exists("./images")
    assert os.path.exists("./images/1.png")
    screenshot.takeScreenShot("https://www.reddit.com/r/csMajors/comments/zn6k7r/recruiter_call_wasted_me_whole_30_mins_and_tells/")
    screenshot.closeDriver()
    assert os.path.exists("./images/2.png")
    os.remove("./images/2.png")
    os.remove("./images/1.png")
    os.rmdir("./images")
    print("Screenshot Test Passed")

invalidPathTest()
invalidUrlTest()
screenshotTest()