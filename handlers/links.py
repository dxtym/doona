import os
import random
from pytube import YouTube
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from utils.config import STICKERS

router = Router()


@router.message(F.text.startswith("https"))
async def link_handler(message: Message) -> None:
    link_encoded = message.text.removeprefix("https://")
    match message.text.split(".")[1]:
        case "youtube":
            yt = YouTube(link_encoded)
            caption_text = f"<b>Title: </b>{yt.title}\n\n<b>By: </b>{yt.author}"
            video = yt.streams.get_highest_resolution()
            file_path = os.path.join("temp", f"{message.from_user.id}.mp4")
            video.download(filename=file_path)
            await message.answer_video(FSInputFile(file_path), caption=caption_text)
            await message.answer("🍟 Do you have nothing else to do?")
            os.remove(file_path)
        case _:
            await message.answer_sticker(random.choice(STICKERS))
