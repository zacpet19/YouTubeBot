import os
from typing import Tuple, List, Any
import praw


class RedditScraper:
    def __init__(self,client_id,client_secret, user_agent):
        self.reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)

    def getTopPostComments(self, subreddit : str) -> tuple[list[list[str]], list[str]]:
        """getTopPostComments takes in the name of the subreddit and then returns a tuple that contains a 2d array of posts
        and comments as well as a list of urls"""
        topComments = []
        urlArray = []
        for post in self.reddit.subreddit(subreddit).hot(limit=20):
            if(len(topComments) > 4):
                break
            if (post.stickied or post.url.endswith(('jpg', 'jpeg', 'png', 'gif'))):
                continue
            parsedBody = self.parsePostBody(post.selftext)
            if(parsedBody == "error"):
                continue
            tempList = []
            post.comments.replace_more(limit=0)
            tempList.append(post.title)
            tempList.append(parsedBody)
            urlArray.append(post.url)
            count = 0
            for top_level_comment in post.comments:
                if(top_level_comment.stickied):
                    continue
                parsed = self.parseComments(top_level_comment.body)
                if parsed == "error":
                    continue
                tempList.append(parsed)
                count += 1
                #Only pull 5 top comments
                if count > 5:
                    break
            topComments.append(tempList)
        print(topComments)
        return (topComments, urlArray)

    #TODO: for both parsers make sure to remove \n and \ before apostrphes maybe
    @staticmethod
    def parseComments(comment : str) -> str:
        if(len(comment) > 1000):
            return "error"
        f = open("bannedWordList.txt","r")
        lines = f.readlines()
        for line in lines:
            comment = comment.replace(line,"*" * len(line))
        return comment

    @staticmethod
    def parsePostBody(body : str) -> str:
        if(len(body) > 2500):
            return "error"
        f = open("bannedWordList.txt", "r")
        lines = f.readlines()
        for line in lines:
            body = body.replace(line, "*" * len(line))
        return body




