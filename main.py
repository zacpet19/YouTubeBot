import redditScraper
from TextToSpeech import TextToSpeech
def main():
    comments = redditScraper.getTopPostComments("csmajors")
    TextToSpeech.textToSpeech(comments)

if __name__ == '__main__':
    main()

