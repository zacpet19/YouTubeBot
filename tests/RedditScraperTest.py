
import sys
sys.path.append('..')
import redditScraper

def getTopPostCommentsTest():
    comments = redditScraper.getTopPostComments("ProgrammerHumor")
    assert len(comments) != 0
    assert type(comments) == list
    assert type(comments[0]) == list
    assert comments[0][0] != comments[1][0]
    for i in comments:
        for j in i:
            assert type(j) == str


if __name__ == "__main__":
    getTopPostCommentsTest()