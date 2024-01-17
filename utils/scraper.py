import os
import re
import json
from config import COURSE_PATTERN
from collections import defaultdict
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()
COURSE_PATTERN = re.compile(fr"{COURSE_PATTERN}")


def fill_timetable(day: str, subject: str, type_: str) -> None:
    path_ = "../data/timetable.json"
    if os.path.exists(path_):
        try:
            with open(path_, "r") as f:
                timetable = json.loads(f.read())
        except json.JSONDecodeError:
            timetable = defaultdict(list)
    else:
        raise FileNotFoundError("File not found")
    
    try:
        timetable[day].append({"subject": subject, "type": type_})
    except KeyError:
        timetable[day] = [{"subject": subject, "type": type_}]

    with open(path_, "w") as f:
        json.dump(timetable, f, indent=4)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()
driver.get(os.getenv("SCRAPE_URL"))

driver.find_element(By.ID, "user").send_keys(os.getenv("SCRAPE_USERNAME"))
driver.find_element(By.ID, "pass").send_keys(os.getenv("SCRAPE_PASSWORD"))
driver.find_element(By.CLASS_NAME, "btn").click()

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
lessons = defaultdict(list)

for weekday in weekdays:
    day = driver.find_element(By.ID, weekday).get_attribute("innerHTML")
    soup = BeautifulSoup(day, 'html.parser')
    slots = soup.find_all("div", class_="innerbox")
    for slot in slots:
        divs = slot.find_all("div")
        for div in divs:
            match_ = COURSE_PATTERN.search(div.get_text().strip())
            if match_:
                lessons[weekday].append({
                    "subject": match_.group(0).split('_')[0], "type": "Lecture" if "lec" in match_.group(0).split('_') else "Seminar"
                })

for key, value in lessons.items():
    for lesson in value:
        fill_timetable(key, lesson["subject"], lesson["type"])

driver.close()
