YouTubeBot README

Overall Description: The YouTubeBot is a program that pulls Reddit posts and then uses them to create videos and upload
them to YouTube. Most of the methods are geared towards creating YouTube shorts. The main program using Praw will pull
Reddit posts, some of its comments, and use Selenium to screen shot the posts. Mp3 files are created using gTTS. Then
background video and audio are formatted for YouTube shorts using the Text to Speech mp3 file(s). The screen shots of
the posts are resized using Pillow. Then the images are turned into videos. Finally, the newly formatted mp3 and mp4
files will be turned into a final video. All video, audio, and image to video formatting is done using MoviePy. Then
the video is uploaded to YouTube using Selenium.

Link to YouTube channel: https://www.youtube.com/@jamesano
Videos will look like the newer ones on this YouTube page

IMPORTANT: This is not yet a finished project. It can currently create and upload YouTube shorts. However, functionality
is limited and has bugs that make it occasionally not work as intended.

Known bugs:
Some audio clips after combining will have "brrt" sound at the end
YouTube will occasionally require 2-factor authentication even when disabled causing upload process to fail
Fails to log into gmail when faced with anti-bot countermeasures
Selenium will occasionally fail and then work under similar circumstances

TODO:
Change Reddit scraper return structure
Add second passthrough of docstrings
implement logger into classes
Write tests for new text to speech methods
write tests for new video methods
Implement better censorship method
Benchmark censorship methods
Use selenium to add tags to youtube shorts
Implement proxy rotation to avoid google CAPTCHA
Make method that changes audio pitch
Make constructor method for Audio class?
Make constructor method for Video class?
Make logs carry over
Give selenium better error handling
Ignore posts about certain things