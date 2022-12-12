import os 
import praw
from dotenv import load_dotenv
load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
user_agent = os.getenv('user_agent')

reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)


def getTopPostComments(subreddit : str) -> list[str]:
    topComments = []
    for post in reddit.subreddit(subreddit).hot(limit=20):
        if(len(topComments) > 4):
            break
        if (post.stickied or post.url.endswith(('jpg', 'jpeg', 'png', 'gif'))):
            continue
        parsedBody = parsePostBody(post.selftext)
        if(parsedBody == "error"):
            continue
        tempList = []
        post.comments.replace_more(limit=0)
        tempList.append(post.title)
        tempList.append(parsedBody)
        count = 0
        for top_level_comment in post.comments:
            if(top_level_comment.stickied):
                continue
            parsed = parseComments(top_level_comment.body)
            if parsed == "error":
                continue
            tempList.append(parsed)
            count += 1
            #Only pull 5 top comments
            if count > 5:
                break
        topComments.append(tempList)
    print(topComments)
    return topComments

#TODO: for both parsers make sure to remove \n and \ before apostrphes maybe
def parseComments(comment : str) -> str:
    if(len(comment) > 1000):
        return "error"
    f = open("bannedWordList.txt","r")
    lines = f.readlines()
    for line in lines:
        comment = comment.replace(line,"*" * len(line))
    return comment

def parsePostBody(body : str) -> str:
    if(len(body) > 2500):
        return "error"
    f = open("bannedWordList.txt", "r")
    lines = f.readlines()
    for line in lines:
        body = body.replace(line, "*" * len(line))
    return body

getTopPostComments("csmajors")


