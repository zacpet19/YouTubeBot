from datetime import datetime
import os
from dotenv import load_dotenv


class Logger:


    def __init__(self):
        load_dotenv()

        projectPath = os.getenv('projectPath')
        filename = f"{projectPath}/logs.txt"

        if not os.path.exists(filename):
            os.makedirs("./logs.txt")

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

    def manageLogFile(self, maxLogs : int, bytesPerLog : int):
        load_dotenv()

        projectPath = os.getenv('projectPath')
        filename = f"{projectPath}/logs.txt"

        if os.path.exists(filename):
            if os.stat(filename).st_size > bytesPerLog:
                if os.path.exists(f"{projectPath}/old_logs{maxLogs}.txt"):
                    os.remove(f"{projectPath}/old_logs{maxLogs}.txt")
                    #taking into account new max logs number deletes all max logs exceeding it
                    count = maxLogs + 1
                    while os.path.exists(f"{projectPath}/old_logs{count}.txt"):
                        os.remove(f"{projectPath}/old_logs{count}.txt")
                        count += 1
                #renames all the old logs to show which ones are newer
                count = maxLogs - 1
                while count > 0:
                    if os.path.exists(f"{projectPath}/old_logs{count}.txt"):
                        os.rename(f"{projectPath}/old_logs{count}.txt", f"{projectPath}/old_logs{count + 1}.txt")
                    count -= 1
                os.rename(filename, f"{projectPath}/old_logs1.txt")

