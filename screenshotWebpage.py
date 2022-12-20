from selenium import webdriver
from PIL import Image
import io
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class ScreenShot:

    def __init__(self, path):
        try:
            ser = Service(path)
            self.driver = webdriver.Chrome(service=ser, options=webdriver.ChromeOptions())
        except Exception as e:
            print("Error: Incorrect path to Chrome Driver.")
            self.driver.quit()
            raise e

    def takeScreenShot(self, urls : [str]):
        """function(url) -> None, saves screenshot in ./images directory"""
        count = 1
        for url in urls:
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
            im.save(f"./images/{count}.png")
            count += 1

    def uploadYoutubeVideo(self, channel : str, username : str, password : str, filepath : str, videoInfo : dict):
        enter = Keys.ENTER
        try:
            self.driver.get(channel)
        except Exception as e:
            print("Youtube channel not found.")
            raise e
        wait = WebDriverWait(self.driver, 10)
        #this try block is here to make the program end if the page takes to long to load
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//ytd-button-renderer[@class='style-scope ytd-masthead']//a[@aria-label='Sign in']//div[@class='yt-spec-touch-feedback-shape__fill']")))
        except Exception as e:
            print("Sign in not found or Webpage took too long to load")
            raise e
        '#this Xpath thing may need to be changed because any slight change to it would ruin the entire program'
        elementToMoveTo = self.driver.find_element(By.XPATH, "//ytd-button-renderer[@class='style-scope ytd-masthead']//a[@aria-label='Sign in']//div[@class='yt-spec-touch-feedback-shape__fill']")
        action = ActionChains(self.driver)
        action.move_to_element(elementToMoveTo).double_click().perform()
        #this is to make it wait for the webpage to load before typing anything in pretty sure any kind of element
        #search would work here
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#identifierIddddddd")))
        except Exception as e:
            print("CSS selector not found on Gmail login page or took too long to load")
            raise e
        action.send_keys(username).send_keys(enter).perform()
        action.pause(2).perform()
        action.send_keys(password).send_keys(enter).perform()
        action.pause(5).perform()
        elementToMoveTo = self.driver.find_element(By.ID, 'upload-video-button')
        action.move_to_element(elementToMoveTo).double_click().perform()
        action.pause(5)
        action.send_keys(enter).perform()
        "# have to send a file using the driver instead of the ActionChains object for some reason"
        self.driver.find_element(By.XPATH, '//*[@id="content"]/input').send_keys(filepath)
        action.pause(10)
        action.send_keys(videoInfo["Title"]).perform()
        action.pause(20).perform()
    def closeDriver(self):
        self.driver.quit()
