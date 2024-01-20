import os
import logging
from dotenv import load_dotenv
from aiogram import Router
from aiogram.types import Message
from llamaapi import LlamaAPI
from utils.config import LLAMA_MESSAGE

load_dotenv()
llama = LlamaAPI(os.getenv('API_KEY'))
router = Router()

@router.message()
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