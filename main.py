import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from llamaapi import LlamaAPI

TOKEN = "6970181638:AAGn60KouG0PfzC9ZC-sGdHi3WVKw0GBTfI"
API = "LL-QNtNcVGtlWyrmKX4cfeomcKO08b4x0qxcX8jYqOKkceKtGINXl5HDaLktxFDCfd9"

dp = Dispatcher()
llama = LlamaAPI(API)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_message_handler(message: Message) -> None:
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


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())