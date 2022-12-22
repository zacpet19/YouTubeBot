from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips
from moviepy.video.VideoClip import ImageClip
import moviepy.video.fx.all as vfx
import os


class VideoMethods:
    @staticmethod
    def setVideoDurationAndRemoveAudio(videoPath : str, duration : int, startCut=0):
        """Takes in a filepath to a mp4 file and then makes it the input duration. If the video is longer than the
        duration it cuts the end of the video to the given duration and if the video is shorter than the given
        duration it loops it until it is long enough. The startCut parameter allows for choosing when to start the
        video."""
        if not os.path.exists("./video"):
            os.makedirs("./video")
        try:
            clip = VideoFileClip(videoPath)
        except Exception as e:
            print("Error: Could not find file.")
            return False
        if startCut > clip.duration:
            print("Error: startCut is greater than the length of the clip.")
        if startCut + duration < clip.duration:
            cutClip = clip.subclip(startCut, duration)
            cutClip.write_videofile("video/silentVideo.mp4", audio=False)
            cutClip.close()
        else:
            if startCut != 0:
                firstHalf = clip.subclip(0, startCut)
                secondHalf = clip.subclip(startCut, clip.duration)
                concat = concatenate_videoclips([secondHalf, firstHalf])
                final = concat.fx(vfx.loop, duration=duration) #ignore IDE about no reference to loop method
                final.write_videofile("video/silentVideo.mp4", audio=False)
                firstHalf.close()
                secondHalf.close()
                concat.close()
                final.close()
            else:
                loopedVideo = clip.fx(vfx.loop, duration=duration) #ignore IDE about no reference to loop method
                loopedVideo.write_videofile("video/silentVideo.mp4", audio=False)
                loopedVideo.close()
        clip.close()

    @staticmethod
    def createImageVideo(imagePath : str, duration : int):
        """IMPORTANT:Image passed in must have even dimensions or the video made will be black!!!!"""
        if not os.path.exists("./video"):
            os.makedirs("./video")
        try:
            clip = ImageClip(imagePath, duration=duration)
        except Exception as e:
            print("Error: Could not find file.")
            return False
        clip.write_videofile("video/imageVideo.mp4", fps=24)
        clip.close()




