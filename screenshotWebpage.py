from selenium import webdriver
from PIL import Image
import io
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

class ScreenShot:

    def __init__(self, path):
        self.count = 1
        try:
            ser = Service(path)
            self.driver = webdriver.Chrome(service=ser, options=webdriver.ChromeOptions())
        except Exception as e:
            print("Error: Incorrect path to Chrome Driver.")
            self.driver.quit()
            raise e

    def takeScreenShot(self, url):
        """function(url) -> None, saves screenshot in ./images directory"""
        try:
            self.driver.get(url)
        except Exception as e:
            print("Error: Failed to access URL")
            raise e
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='post-container']")
        except Exception as e:
            print("Error: failed to find CSS element on webpage")
            raise e
        image = element.screenshot_as_png
        imageStream = io.BytesIO(image)
        im = Image.open(imageStream)
        if not os.path.exists("./images"):
            os.makedirs("./images")
        im.save(f"./images/{self.count}.png")
        self.count += 1


    def closeDriver(self):
        self.driver.quit()
