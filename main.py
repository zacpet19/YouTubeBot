import redditScraper
from TextToSpeech import TextToSpeech
from screenshotWebpage import ScreenShot
def main():
    (comments, urls) = redditScraper.getTopPostComments("csmajors")
    screenShotter = ScreenShot("a")
    screenShotter.takeScreenShot(urls)
    screenShotter.closeDriver()
    TextToSpeech.textToSpeech(comments)

if __name__ == '__main__':
    main()

