import os
from typing import Tuple, List, Any
import praw


class RedditScraper:
    def __init__(self,client_id,client_secret, user_agent):
        self.reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)
        self.shouldCensor = False
        self.pastUrls = set()
        try:
            f = open("visitedRedditPages.txt", "r")
            lines = f.readlines()
            for line in lines:
                self.pastUrls.add(line.replace("\n", ""))
        except Exception:
            print("Failed to open visitedRedditPages.txt, duplicate posts may be used")
        #Check if bannedWordList exists
        try:
            f = open("bannedWordList.txt", "r")
            f.close()
            self.shouldCensor = True
        except Exception:
            print("Failed to open bannedWordList.txt, reddit text will not be censored")

        

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
            if (post.url in self.pastUrls):
                continue
            parsedBody = self.parsePostBody(post.selftext)
            #If body is too long we move to next post
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
                #Ignore comments that are too long
                if parsed == "error":
                    continue
                tempList.append(parsed)
                count += 1
                #Only pull 5 top comments
                if count > 5:
                    break
            topComments.append(tempList)
        print(topComments)
        #Document visited urls to avoid duplicate 
        f = open("visitedRedditPages.txt", "a")
        for url in urlArray:
            f.write(url + "\n")
        f.close()

        return (topComments, urlArray)


    def parseComments(self,comment : str) -> str:
        """TODO: Not currently censoring all the bad words. FIX"""
        if(len(comment) > 1000):
            return "error"
        if not self.shouldCensor:
            return comment
        f = open("bannedWordList.txt","r")
        lines = f.readlines()
        for line in lines:
            comment = comment.replace(line,"*" * len(line))
        f.close()
        return comment


    def parsePostBody(self,body : str) -> str:
        if(len(body) > 2500):
            return "error"
        if not self.shouldCensor:
            return body
        f = open("bannedWordList.txt", "r")
        lines = f.readlines()
        for line in lines:
            body = body.replace(line, "*" * len(line))
        f.close()
        return body




