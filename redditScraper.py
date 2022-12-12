import os 
import praw
from dotenv import load_dotenv
load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
user_agent = os.getenv('user_agent')

reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)


def getTopPost(subreddit : str) -> list[str]:
    for submission in reddit.subreddit(subreddit).hot(limit=4):
        print(submission.title)

getTopPost("ProgrammerHumor")