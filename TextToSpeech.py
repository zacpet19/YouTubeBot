from gtts import gTTS
import os 

class TextToSpeech:
    @staticmethod
    def textToSpeech(text):
        if not os.path.exists("./audio"):
            os.makedirs("./audio")
        count = 1
        for i in text:
            stringBuilder = ""
            for j in i:
                stringBuilder += j
            audio = gTTS(text=stringBuilder,lang = "en", slow=False, tld = "US")
            audio.save(f"./audio/{count}.mp3")
            count += 1




