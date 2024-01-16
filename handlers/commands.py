import os
import logging
import requests
from dotenv import load_dotenv
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.utils.markdown import hbold
from keyboards.todo import todo_keyboard
from utils.config import LAT, LONG
from utils.timetable import show_timetable

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
        f"📝 Things you've to finish:\n",
        reply_markup=todo_keyboard
    )

@router.message(Command("timetable"))
async def command_timetable_handler(message: Message) -> None:
    try:
        await message.answer(show_timetable())
    except Exception as e:
        logging.error(e)
        await message.answer("❌ Something went wrong!")


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

        await message.answer(f"⛅ You're so lazy...\nSummary: {weather}\nTemperature: {temp}°C\nHumidity: {humidity}%")
    except Exception as e:
        logging.error(e)
        await message.answer("❌ Something went wrong!")


@router.message(Command("waifu"))
async def command_waifu_handler(message: Message) -> None:
    try:
        url = "https://api.waifu.pics/sfw/waifu"
        response = requests.get(url).json()
        await message.reply_photo(response["url"])
    except Exception as e:
        logging.error(e)
        await message.answer("❌ Something went wrong!")


@router.message(Command("stop"))
async def command_stop_handler(message: Message) -> None:
    await message.answer_sticker(
        "CAACAgIAAxkBAAELLL9lo4tpheuEG46rhHY3MnbhFK8ibgACPBgAAnHMfRjAnBo1wPnRDzQE", 
        protect_content=True
        )
    await message.answer("👋 Never come back, okay?")