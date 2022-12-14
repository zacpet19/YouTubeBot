import os
from dotenv import load_dotenv
import sys
sys.path.append('..')
from src.redditScraper import RedditScraper


def getTopPostCommentsTest():
    load_dotenv()
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    user_agent = os.getenv('user_agent')

    reddit = RedditScraper(client_id,client_secret,user_agent)
    (comments,urls, _) = reddit.getTopPostAndComments("csmajors", 2)
    assert len(urls) != 0
    assert type(urls) == list
    assert type(urls[0]) == str
    assert len(comments) != 0
    assert type(comments) == list
    assert type(comments[0]) == list
    assert comments[0][0] != comments[1][0]
    for i in comments:
        #figure out what enumerate actually does?????
        for index, j in enumerate(i):
            assert type(j) == str
            if index == 1:
                assert len(j) <= 2500
                assert "http" not in j
                assert "!!" not in j
                assert "??" not in j
                assert ".." not in j
                f = open("bannedWordList.txt", "r")
                lines = f.readlines()
                for line in lines:
                    assert line not in j
            if index > 1:
                assert len(j) <= 1000
                f = open("bannedWordList.txt","r")
                lines = f.readlines()
                for line in lines:
                    assert line not in j

    print("TopPostCommentsTest Passed")

def parseTest():
    badText = " Here is the the wiki link to it https://en.wikipedia.org/wiki/White_Rock"
    load_dotenv()
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    user_agent = os.getenv('user_agent')

    reddit = RedditScraper(client_id,client_secret,user_agent)

    print(reddit.parseComments(badText))
    print("Parse test passed")

    


if __name__ == "__main__":
    getTopPostCommentsTest()
    parseTest()