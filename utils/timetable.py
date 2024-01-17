import os
import json
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.utils.markdown import hbold, hitalic
from collections import defaultdict

load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")


def show_timetable() -> str:
    with open("./data/timetable.json", "r") as f:
        classes = json.loads(f.read())
    if not classes:
        return "🍜 No classes today, chill!"
    else:
        timetable = defaultdict(str)
        message = "📋 Check the timetable yourself, nerd! \n"
        for day, class_ in classes.items():
            for slot in class_:
                timetable[day] += f"{slot['subject']} - {slot['type']}\n"
        for weekday, classes in timetable.items():
            message += f"{hbold(weekday)}: \n{hitalic(classes)}\n"
        return message


async def show_timetable_by_day(bot: Bot, day: str) -> None:
    with open("./data/timetable.json", "r") as f:
        classes = json.loads(f.read())
    if not classes:
        await bot.send_message(CHAT_ID, f"🍜 No classes on {day}, chill!")
    else:
        message = ""
        for slot in classes[day]:
            message += f"{hitalic(slot['subject'])} - {hitalic(slot['type'])}\n"
        await bot.send_message(CHAT_ID, f"📋 No rest for you on {day}! \n{message}")
