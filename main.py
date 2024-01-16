import os
import asyncio
import logging
import sys
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from callbacks import tasks
from utils.timetable import show_timetable_by_day
from utils.weather import show_daily_weather
from handlers import commands, messages, photos

load_dotenv()


async def main() -> None:
    bot = Bot(os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(
        commands.router,
        photos.router,
        tasks.router,
        messages.router
    )
    await bot.set_my_commands([
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/todo", description="Manage all tasks"),
        BotCommand(command="/timetable", description="View weekly timetable"),
        BotCommand(command="/weather", description="Check out the weather"),
        BotCommand(command="/waifu", description="Get a random waifu"),
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
