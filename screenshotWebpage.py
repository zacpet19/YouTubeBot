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
        self.driver.maximize_window()
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
        """this method takes in a url to a channel, a gmail username/password, a filepath to the mp4 you would like
        to upload, and a dictionary containing video info on the tital and description. Then it uses selenium to upload
        the video to the youtube channel provided"""
        """TODO Make it possible to add tags and do way more exception handling"""
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
        attempts = 0
        #while loop attempts to input the gmail 5 times and errors if it doesnt work
        '#TODO: Consider adding something that deletes the previous attempt'
        while attempts < 5:
            action.send_keys(username).perform()
            try:
                attempts += 1
                WebDriverWait(self.driver, 2).until(EC.text_to_be_present_in_element_value((By.NAME, "identifier"), username))
                action.send_keys(enter).perform()
                break
            except Exception as e:
                if attempts >= 5:
                    print("Element name not found on Gmail login page or took too long to load")
                    raise e
        attempts = 0
        #while loop will try to enter the password until it finds that the password is present in the page and after 5
        #attempts it will stop and end the program
        while attempts < 5:
            action.send_keys(password).perform()
            try:
                attempts += 1
                WebDriverWait(self.driver, 2).until(EC.text_to_be_present_in_element_value((By.NAME, "Passwd"), password))
                action.send_keys(enter).perform()
                break
            except Exception as e:
                if attempts >= 5:
                    print("Element name not found on Gmail login page or took too long to load")
                    raise e
        #makes sure the page is loaded up and the button can be clicked on before doing the clicking action
        try:
            elementToMoveTo = wait.until(EC.element_to_be_clickable((By.ID, "edit-buttons")))
        except Exception as e:
            print("Couldn't locate provided element or page took too long to load")
            raise e
        action.move_to_element(elementToMoveTo).perform()
        action.move_by_offset(yoffset=0, xoffset=100).click().perform()
        #swicthes the driver to work out of the new window that was just opened
        attempts = 0
        while attempts < 5:
            try:
                attempts += 1
                self.driver.switch_to.window(self.driver.window_handles[1])
            except Exception as e:
                print("Page took to long to load.")
                action.pause(3).perform()
                if attempts >= 5:
                    raise e
        try:
            elementToMoveTo = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, "create-icon")))
        except Exception as e:
            print("Couldn't locate provided element or page took too long to load")
            raise e
        action.click(elementToMoveTo).perform()
        action.move_by_offset(yoffset=32, xoffset=0).click().perform()
        attempts = 0
        #while loop tries to upload the video the enter key is to get rid of potential popups since if there is 0 popups
        #the enter key does nothing on that screen
        while attempts < 5:
            action.send_keys(enter).perform()
            "# have to send a file using the driver instead of the ActionChains object for some reason"
            self.driver.find_element(By.XPATH, '//*[@id="content"]/input').send_keys(filepath)
            try:
                wait.until(EC.element_to_be_clickable((By.ID, 'textbox')))
                break
            except Exception as e:
                print("Couldn't locate provided element or page took too long to load")
                raise e
        action.pause(10)
        action.send_keys(videoInfo["Title"]).perform()
        elementToMoveTo = self.driver.find_element(By.ID, "description-container")
        action.click(elementToMoveTo).send_keys(videoInfo["Description"]).perform()
        #this part and the next try block might not actually be doing anything and is unceccassary
        #this is suppose to pick a randomly generated youtube thumbnail but it might no even need to pick one
        """elementToMoveTo = self.driver.find_element(By.ID, "still-picker")
        action.scroll_to_element(elementToMoveTo).perform()
        attempts = 0
        while attempts < 5:
            try:
                attempts += 1
                WebDriverWait(self.driver, 6).until(EC.element_to_be_clickable((elementToMoveTo)))
                print("element is clickable")
                break
            except Exception as e:
                if attempts >= 5:
                    print("Couldn't locate provided element or page took too long to load")
                    raise e
        action.click(elementToMoveTo).perform()
        """
        #these next two lines dont do anything as of right now but is necessary to add tags at a later point
        elementToMoveTo = self.driver.find_element(By.ID, "toggle-button")
        action.scroll_to_element(elementToMoveTo).perform()
        elementToMoveTo = self.driver.find_element(By.ID, "offRadio")
        action.move_to_element(elementToMoveTo).perform()
        action.move_by_offset(yoffset=25, xoffset=0).click().perform()
        elementToMoveTo = self.driver.find_element(By.ID, "toggle-button")
        action.scroll_to_element(elementToMoveTo).click(elementToMoveTo).perform()
        elementToMoveTo = self.driver.find_element(By.ID, "next-button")
        action.click(elementToMoveTo).perform()
        action.click(elementToMoveTo).perform()
        action.click(elementToMoveTo).perform()
        elementToMoveTo = self.driver.find_element(By.NAME, "PUBLIC")
        action.click(elementToMoveTo).perform()
        #this will definitely need some error handling due to Youtube taking awhile to verify your youtube video isnt
        #copywright infringement
        elementToMoveTo = self.driver.find_element(By.ID, "done-button")
        action.click(elementToMoveTo).perform()
        action.pause(20).perform()

    def closeDriver(self):
        self.driver.quit()
