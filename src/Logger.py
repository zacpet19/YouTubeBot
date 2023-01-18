from datetime import datetime


class Logger:


    def __init__(self):
        self.name = "Epic logger"
        self.logFile = open("logs.txt","a", encoding="utf-8")
    
    def debug(self, string: str):
        text = f"[{self.getTime()}][DEBUG] {string}"
        self.logFile.write(text + '\n')
        print(text)

    def info(self, string: str):
        text = f"[{self.getTime()}][INFO] {string}"
        print(text)
        self.logFile.write(text + '\n')

    def warn(self, string: str):
        text = f"[{self.getTime()}][WARN] {string}"
        print(text)
        self.logFile.write(text + '\n')

    def error(self, string: str):
        text = f"[{self.getTime()}][ERROR] {string}"
        print(text)
        self.logFile.write(text + '\n')

    def getTime(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")



    



