import os
import random
import aiofiles
from pytube import YouTube
from aiogram import Router, F
from aiogram.types import Message, InputFile
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
            await message.reply_photo(yt.thumbnail_url, caption=caption_text)
            await message.answer("🍟 Do you have nothing else to do?")
            file_path = os.path.join("temp", f"{message.from_user.id}.mp4")
            video.download(filename=file_path)
            async with aiofiles.open(file_path, "rb") as video_file:
                await message.answer_video(InputFile(video_file))
            os.remove(file_path)
        case "tiktok":
            # TODO: Add download TikTok support
            await message.answer("🎈 I don't have time to scroll TikTok")
        case "instagram":
            # TODO: Add download Instagram support
            await message.answer("🎈 I don't have time to scroll Instagram")
        case _:
            await message.answer(random.choice(STICKERS))
