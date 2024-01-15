import os
import sqlite3 as sql

from dotenv import load_dotenv
from aiogram import Bot
from aiogram.utils.markdown import hbold, hitalic
from collections import defaultdict

load_dotenv()

CHAT_ID = os.getenv("CHAT_ID")

db = sql.connect("data/timetable.db")
cursor = db.cursor()


def show_timetable() -> str:
    cursor.execute("SELECT * FROM timetable")
    classes = cursor.fetchall()
    if not classes:
        return "🍜 No classes today"
    else:
        timetable = defaultdict(str)
        message = "📋 Timetable: \n"
        for class_ in classes:
            timetable[class_[0]] += f"{class_[1]} - {class_[2]}\n"
        for weekday, classes in timetable.items():
            message += f"{hbold(weekday)}: \n{classes}\n"
        return message


async def show_timetable_by_day(bot: Bot, day: str) -> None:
    cursor.execute(f"SELECT * FROM timetable WHERE day='{day}'")
    classes = cursor.fetchall()
    if not classes:
        await bot.send_message(CHAT_ID, f"🍜 No classes on {day}")
    else:
        message = ""
        for index, class_ in enumerate(classes):
            message += f"{index+1}. {class_[1]} - {hitalic(class_[2])}\n"
        await bot.send_message(CHAT_ID, f"📋 Timetable for {day}: \n{message}")
