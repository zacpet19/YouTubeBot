from selenium import webdriver
from PIL import Image
import io
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

ser = Service()
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)
url = "https://www.reddit.com/r/csMajors/comments/zn6k7r/recruiter_call_wasted_me_whole_30_mins_and_tells/"


driver.get(url)
element = driver.find_element(By.CSS_SELECTOR, "[data-testid='post-container']")
image = element.screenshot_as_png

imageStream = io.BytesIO(image)
im = Image.open(imageStream)
im.save("a.png")

driver.quit()