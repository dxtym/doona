import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()
driver.get(os.getenv("SCRAPE_URL"))

driver.find_element(By.ID, "user").send_keys(os.getenv("SCRAPE_USERNAME"))
driver.find_element(By.ID, "pass").send_keys(os.getenv("SCRAPE_PASSWORD"))
driver.find_element(By.CLASS_NAME, "btn").click()

time.sleep(5)

# driver.close()