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

class WebHandler:
    """This class is contains general methods for using selenium to interact with the Google Chrome."""
    def __init__(self, path):
        """Creates an object with the Selenium chrome driver. Takes in the file path to the chrome driver."""
        try:
            ser = Service(path)
            self.driver = webdriver.Chrome(service=ser, options=webdriver.ChromeOptions())
        except Exception as e:
            print("Error: Incorrect path to Chrome Driver.")
            self.driver.quit()
            raise e

    def screenShotRedditPosts(self, urls : list[str]):
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
        to upload, and a dictionary containing video info on the title and description. Then it uses selenium to upload
        the video to the YouTube channel provided. IMPORTANT: Does not work with 2 factor identification!!!"""
        """TODO Make it possible to add tags and do way more exception handling"""
        enter = Keys.ENTER
        #searching for youtube page
        try:
            self.driver.get(channel)
        except Exception as e:
            print("Youtube channel not found.")
            raise e
        wait = WebDriverWait(self.driver, 10)
        #clicking on the sign in button
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//ytd-button-renderer[@class='style-scope ytd-masthead']//a[@aria-label='Sign in']//div[@class='yt-spec-touch-feedback-shape__fill']")))
        except Exception as e:
            print("Sign in not found or Webpage took too long to load")
            raise e
        #clicking on sign in box
        elementToMoveTo = self.driver.find_element(By.XPATH, "//ytd-button-renderer[@class='style-scope ytd-masthead']//a[@aria-label='Sign in']//div[@class='yt-spec-touch-feedback-shape__fill']")
        action = ActionChains(self.driver)
        action.move_to_element(elementToMoveTo).double_click().perform()
        attempts = 0
        #Typeing in username/email
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
        #Typing in password
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
        #clicking on the manage videos button
        try:
            elementToMoveTo = wait.until(EC.element_to_be_clickable((By.ID, "edit-buttons")))
        except Exception as e:
            print("Couldn't locate provided element or page took too long to load")
            raise e
        action.move_to_element(elementToMoveTo).perform()
        action.move_by_offset(yoffset=0, xoffset=100).click().perform()
        #switching to the newly opened window
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
        #clicking video creation button
        try:
            elementToMoveTo = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, "create-icon")))
        except Exception as e:
            print("Couldn't locate provided element or page took too long to load")
            raise e
        action.click(elementToMoveTo).perform()
        action.move_by_offset(yoffset=32, xoffset=0).click().perform()
        attempts = 0
        #sending video for upload
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
        #video frequently takes a bit to upload so it pauses for 10 seconds no matter what might need to be longer for
        #bad connections and larger videos
        action.pause(10)
        #typing Youtube video title
        action.send_keys(videoInfo["Title"]).perform()
        #typing Youtube video description
        elementToMoveTo = self.driver.find_element(By.ID, "description-container")
        action.click(elementToMoveTo).send_keys(videoInfo["Description"]).perform()
        #this is suppose to pick a randomly generated youtube thumbnail but Youtube can pick on automatically
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
        #clicks button that says video is not made for kids
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
        #makes video viewable by public
        elementToMoveTo = self.driver.find_element(By.NAME, "PUBLIC")
        action.click(elementToMoveTo).perform()
        #completes upload of video
        elementToMoveTo = self.driver.find_element(By.ID, "done-button")
        action.click(elementToMoveTo).perform()
        action.pause(20).perform()

    def closeDriver(self):
        """Closes the selenium web driver."""
        self.driver.quit()
