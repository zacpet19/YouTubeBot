import sys
import os
sys.path.append('..')

from Audio import TextToSpeech

def TexttoSpeechTest():
    comment = [["hello", "goodbye", "Hey there"], ["Hello, GoodBye", "Hey there"]]
    textToSpeech = TextToSpeech.textToSpeech(comment)
    assert os.path.exists("./audio")
    assert os.path.exists("./audio/1.mp3")
    assert os.path.exists("./audio/2.mp3")
    os.remove("./audio/1.mp3")
    os.remove("./audio/2.mp3")
    os.rmdir("./audio")
    print("tests completed")

TexttoSpeechTest()




