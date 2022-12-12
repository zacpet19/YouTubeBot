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
    for post in reddit.subreddit(subreddit).hot(limit=4):
        tempList = []
        post.comments.replace_more(limit=0)
        tempList.append(post.title)
        count = 0
        for top_level_comment in post.comments:
            tempList.append(top_level_comment.body)
            count += 1
            #Only pull 5 top comments
            if count > 5:
                break
        topComments.append(tempList)
    return topComments




getTopPostComments("ProgrammerHumor")