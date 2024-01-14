import os
import asyncio
import logging
import sys
import requests
import random
from datetime import datetime

from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import Message, BotCommand
from aiogram.utils.markdown import hbold

from llamaapi import LlamaAPI
from utils.config import LLAMA_MESSAGE, LAT, LONG, STICKERS
from utils.timetable import show_timetable_by_day, show_timetable
from utils.weather import show_daily_weather



load_dotenv()
dp = Dispatcher()
llama = LlamaAPI(os.getenv('API_KEY'))


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer_sticker(
        "CAACAgIAAxkBAAELLCZlos_v7O7sRX4zAZl2h6BkKmXkhwACDBgAAnHMfRhhqqr6VOP81zQE", 
        protect_content=True
        )
    await message.answer(f"👋 Hello, {hbold(message.from_user.full_name)}-chan!")


@dp.message(Command("waifu"))
async def command_waifu_handler(message: Message) -> None:
    try:
        url = "https://api.waifu.pics/sfw/waifu"
        response = requests.get(url).json()
        await message.reply_photo(response["url"])
    except Exception as e:
        logging.error(e)
        await message.answer("❌ Something went wrong!")


@dp.message(Command("timetable"))
async def command_timetable_handler(message: Message) -> None:
    try:
        await message.answer(show_timetable())
    except Exception as e:
        logging.error(e)
        await message.answer("❌ Something went wrong!")


@dp.message(Command("weather"))
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

        await message.answer(f"⛅ Weather:\nSummary: {weather}\nTemperature: {temp}°C\nHumidity: {humidity}%")
    except Exception as e:
        logging.error(e)
        await message.answer("❌ Something went wrong!")


@dp.message(Command("stop"))
async def command_stop_handler(message: Message) -> None:
    await message.answer_sticker(
        "CAACAgIAAxkBAAELLL9lo4tpheuEG46rhHY3MnbhFK8ibgACPBgAAnHMfRjAnBo1wPnRDzQE", 
        protect_content=True
        )
    await message.answer("👋 Bye-bye!")


@dp.message()
async def echo_message_handler(message: Message) -> None:
    try:
        request = {
            "messages": [
                {
                    "role": "user",
                    "content": LLAMA_MESSAGE + message.text,
                }
            ]
        }

        response = llama.run(request).json()
        await message.reply(response["choices"][0]["message"]["content"])
    except Exception as e:
        logging.error(e)
        await message.reply(message.text)


@dp.message(F.photo)
async def echo_photo_handler(message: Message) -> None:
    await message.answer_sticker(random.choice(STICKERS), protect_content=True)


async def main() -> None:
    bot = Bot(os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
    await bot.set_my_commands([
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/waifu", description="Get a random waifu"),
        BotCommand(command="/timetable", description="View weekly timetable"),
        BotCommand(command="/weather", description="Check out the weather"),
        BotCommand(command="/stop", description="Stop the bot"),
    ])
    scheduler = AsyncIOScheduler(timezone='Asia/Tashkent')
    day = datetime.now().strftime("%A")
    scheduler.add_job(show_timetable_by_day, trigger='cron', hour=6, minute=30, start_date=datetime.now(),
                      args=[bot, day])
    scheduler.add_job(show_daily_weather, trigger='cron', hour=6, minute=30, start_date=datetime.now(),
                      args=[bot]) 
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
