import os
import re
import sqlite3 as sql

from utils.config import COURSE_PATTERN
from collections import defaultdict
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()

COURSE_PATTERN = re.compile(fr"{COURSE_PATTERN}")

db = sql.connect("../data/timetable.db")
cursor = db.cursor()


def start_timetable() -> None:
    cursor.execute("CREATE TABLE IF NOT EXISTS timetable(day TEXT, subject TEXT, type TEXT)")
    db.commit()


def fill_timetable(day: str, subject: str, type: str) -> None:
    cursor.execute(f"INSERT INTO timetable(day, subject, type) VALUES('{day}', '{subject}', '{type}')")
    db.commit()


def show_timetable() -> None:
    cursor.execute("SELECT * FROM timetable")
    return cursor.fetchall()


start_timetable()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()
driver.get(os.getenv("SCRAPE_URL"))

driver.find_element(By.ID, "user").send_keys(os.getenv("SCRAPE_USERNAME"))
driver.find_element(By.ID, "pass").send_keys(os.getenv("SCRAPE_PASSWORD"))
driver.find_element(By.CLASS_NAME, "btn").click()

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
lessons = defaultdict(set)

for weekday in weekdays:
    day = driver.find_element(By.ID, weekday).get_attribute("innerHTML")
    soup = BeautifulSoup(day, 'html.parser')
    slots = soup.find_all("div", class_="innerbox")
    for slot in slots:
        divs = slot.find_all("div")
        for div in divs:
            match_ = COURSE_PATTERN.search(div.get_text().strip())
            if match_:
                lessons[weekday].add(match_.group(0))

for key, value in lessons.items():
    for lesson in value:
        if "lec"in lesson.split('_'):
            fill_timetable(key, lesson.split('_')[0], "Lecture")
        else:
            fill_timetable(key, lesson.split('_')[0], "Seminar")

driver.close()