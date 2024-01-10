import os
import asyncio
import logging
import sys
import requests
from datetime import datetime

from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import Message, BotCommand
from aiogram.utils.markdown import hbold

from llamaapi import LlamaAPI
from utils.timetable import show_timetable_by_day, show_timetable

load_dotenv()
dp = Dispatcher()
llama = LlamaAPI(os.getenv('API_KEY'))


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(Command("waifu"))
async def command_waifu_handler(message: Message) -> None:
    try:
        url = os.getenv("API_URL")
        response = requests.get(url).json()
        await message.reply_photo(response["url"])
    except Exception as e:
        logging.error(e)
        await message.answer("Something went wrong")


@dp.message(Command("timetable"))
async def command_timetable_handler(message: Message) -> None:
    try:
        await message.answer(show_timetable())
    except Exception as e:
        logging.error(e)
        await message.answer("Something went wrong")


@dp.message(Command("support"))
async def command_support_handler(message: Message) -> None:
    await message.answer("Please contact @thisisdilmurod for support")


@dp.message()
async def echo_message_handler(message: Message) -> None:
    try:
        request = {
            "messages": [
                {
                    "role": "user",
                    "content": "Act as my assistant bot - Doona," + message.text,
                }
            ]
        }
        response = llama.run(request).json()
        await message.reply(response["choices"][0]["message"]["content"])
    except Exception as e:
        logging.error(e)
        await message.reply(message.text)


async def main() -> None:
    bot = Bot(os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
    await bot.set_my_commands([
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/waifu", description="Get a random waifu"),
        BotCommand(command="/timetable", description="View weekly timetable"),
        BotCommand(command="/weather", description="Check out the weather"),
        BotCommand(command="/support", description="Call for support"),
    ])
    scheduler = AsyncIOScheduler(timezone='Asia/Tashkent')
    day = datetime.now().strftime("%A")
    scheduler.add_job(show_timetable_by_day, trigger='cron', hour=6, minute=30, start_date=datetime.now(),
                      args=[bot, day]) 
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
