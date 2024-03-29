import os
import re
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from functions import download_tiktok, download_instagram_media
import dotenv
import logging
import requests
import sys
dotenv.load_dotenv()

TOKEN = os.environ.get("TOKEN")
dp = Dispatcher()
download_lock = asyncio.Lock()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("""⚡️ FREE TikTok Downloader """, parse_mode=ParseMode.HTML)


@dp.message()
async def normal_message_handler(message: Message):
    link_url = message.text
    if "instagram" in link_url:
        try:
            querystring = {"url":"https://www.instagram.com/reel/CxgAOUUR8R6/"}

            headers = {
            	"X-RapidAPI-Key": "e9805aa757mshe1542b6585aa5adp165755jsnc846e8890713",
            	"X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
            }

            response = requests.get(link_url, headers=headers, params=querystring)
            await message.answer(response.json().get("media", "Nothing"))
            
        except Exception as e:
            await message.answer(str(e))

    if "tiktok.com" in link_url:
        try:
            video_name = download_tiktok(link_url)
            with open(video_name, "r") as video_file:
                await message.answer_video(video=FSInputFile(video_file.name))
            await message.answer("Video downloaded and sent!")

            async with download_lock:
                os.remove(video_name)
        except Exception as e:
            await message.answer(str(e))


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
