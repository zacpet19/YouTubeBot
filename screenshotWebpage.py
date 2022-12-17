from selenium import webdriver
from PIL import Image
import io

driver = webdriver.Chrome("")

url = "https://www.reddit.com/r/csMajors/comments/zn6k7r/recruiter_call_wasted_me_whole_30_mins_and_tells/"


driver.get(url)
element = driver.find_element_by_css_selector("[data-testid='post-container']")
image = element.screenshot_as_png

imageStream = io.BytesIO(image)
im = Image.open(imageStream)
im.save("a.png")

driver.quit()