from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

"""curently this code is just here for testing and potential future use
load_dotenv()
youtubeAPIKey = os.getenv('youtube_API_Key')
youtube = YouTubeAPIClient(youtubeAPIKey)
request = youtube.youtube.channels().list(part='statistics', forUsername='schafer5')
print(request)"""

class YouTubeAPIClient:
    """this is not really going to be used with our current plans but may be worth keeping around for YouTube data
     analytics or something"""
    def __init__(self, youtubeAPIKey : str):
        try:
            self.youtube = build('youtube', 'v3', developerKey=youtubeAPIKey)
        except Exception as e:
            print("Error: Invalid API key given or unable to connect to client")
            raise e
