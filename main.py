import os
import asyncio
import logging
import sys
import requests

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import Message, BotCommand
from aiogram.utils.markdown import hbold

from llamaapi import LlamaAPI

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


@dp.message()
async def echo_message_handler(message: Message) -> None:
    try:
        request = {
            "messages": [
                {
                    "role": "user",
                    "content": message.text,
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
        BotCommand(command="/support", description="Call for support"),
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())