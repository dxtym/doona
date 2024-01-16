import random
from aiogram import Router, F
from aiogram.types import Message
from utils.config import STICKERS

router = Router()

@router.message(F.photo)
async def echo_photo_handler(message: Message) -> None:
    await message.answer_sticker(random.choice(STICKERS), protect_content=True)