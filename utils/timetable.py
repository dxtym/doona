import os
import sqlite3 as sql
from dotenv import load_dotenv

load_dotenv()
db = sql.connect("database/timetable.db")
cursor = db.cursor()

CHAT_ID = os.getenv("CHAT_ID")

def show_timetable():
    cursor.execute("SELECT * FROM timetable")
    classes = cursor.fetchall()
    if not classes:
        return "No classes today"
    else:
        timetable = {}
        message = ""
        for class_ in classes:
            timetable[class_[0]] = timetable.get(class_[0], "") + f"{class_[1]} - {class_[2]}\n"
        for weekday, classes in timetable.items():
            message += f"{weekday}: \n{classes}\n"
        return message


async def show_timetable_by_day(bot, day):
    cursor.execute(f"SELECT * FROM timetable WHERE day='{day}'")
    classes = cursor.fetchall()
    if not classes:
        await bot.send_message(CHAT_ID, f"No classes on {day}")
    else:
        message = ""
        for index, class_ in enumerate(classes):
            message += f"{index+1}. {class_[1]} - {class_[2]}\n"
        await bot.send_message(CHAT_ID, f"Timetable for {day}: \n{message}")
