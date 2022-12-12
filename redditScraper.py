import os 
import praw
from dotenv import load_dotenv
from profanity_filter import ProfanityFilter
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
        tempList = []
        post.comments.replace_more(limit=0)
        tempList.append(post.title)
        tempList.append(post.selftext)
        count = 0
        for top_level_comment in post.comments:
            if(top_level_comment.stickied):
                continue
            tempList.append(top_level_comment.body)
            count += 1
            #Only pull 5 top comments
            if count > 5:
                break
        topComments.append(tempList)
    print(topComments)
    return topComments

def parseComments(comment : str) -> str:
    if(len(comment) > 1000):
        return "error"
    pf = ProfanityFilter()
    comment = pf.censor(comment)
    return comment

print(parseComments("fuck"))








getTopPostComments("csmajors")