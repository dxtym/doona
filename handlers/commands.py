import os
import json
import logging
import requests
from dotenv import load_dotenv
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from collections import defaultdict
from aiogram.utils.markdown import hbold, hitalic
from keyboards.todo import todo_keyboard
from utils.config import LAT, LONG

load_dotenv()
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer_sticker(
        "CAACAgIAAxkBAAELLCZlos_v7O7sRX4zAZl2h6BkKmXkhwACDBgAAnHMfRhhqqr6VOP81zQE", 
        protect_content=True
        )
    await message.answer(f"👋 It's you again, {hbold(message.from_user.full_name)}!")


@router.message(Command("todo"))
async def command_todo_handler(message: Message) -> None:
    await message.answer(
        f"📝 Stuff you've to finish:\n",
        reply_markup=todo_keyboard
    )


@router.message(Command("timetable"))
async def command_timetable_handler(message: Message) -> None:
    try:
        with open("./data/timetable.json", "r") as f:
            classes = json.loads(f.read())

        if not classes:
            await message.answer("🍜 No classes today, chill!")
        else:
            timetable = defaultdict(str)
            message_ = "📋 Check the timetable yourself, nerd! \n"

            for day, class_ in classes.items():
                for slot in class_:
                    timetable[day] += f"{slot['subject']} - {slot['type']}\n"
            for weekday, classes in timetable.items():
                message_ += f"{hbold(weekday)}: \n{hitalic(classes)}\n"

            await message.answer(message_)
    except Exception as e:
        logging.error(e)
        await message.answer("❌ You sure are a problem, dude!")


@router.message(Command("weather"))
async def command_weather_handler(message: Message) -> None:
    try:
        params = {
            "lat": LAT,
            "lon": LONG,
            "appid": os.getenv("WEATHER_API_KEY"),
            "units": "metric",
        }

        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather", 
            params=params).json()
        weather = response["weather"][0]["main"].capitalize()
        temp = response["main"]["temp"]
        humidity = response["main"]["humidity"]

        await message.answer(f"⛅ Go ask someone else!\nSummary: {weather}\nTemperature: {temp}°C\nHumidity: {humidity}%")
    except Exception as e:
        logging.error(e)
        await message.answer("❌ You sure are a problem, dude!")


@router.message(Command("waifu"))
async def command_waifu_handler(message: Message) -> None:
    try:
        url = "https://api.waifu.pics/sfw/waifu"
        response = requests.get(url).json()

        await message.reply_photo(response["url"])
        await message.answer("👀 What a weeb!")
    except Exception as e:
        logging.error(e)
        await message.answer("❌ You sure are a problem, dude!")


@router.message(Command("stop"))
async def command_stop_handler(message: Message) -> None:
    await message.answer_sticker(
        "CAACAgIAAxkBAAELLL9lo4tpheuEG46rhHY3MnbhFK8ibgACPBgAAnHMfRjAnBo1wPnRDzQE", 
        protect_content=True
        )
    await message.answer("👋 Never come back, okay?")