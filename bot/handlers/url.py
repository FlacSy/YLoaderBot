import logging
import re
from aiogram import types
from utils.download_video import download_tiktok, download_youtube
from utils.download_music import download_spotify, download_soundcloud

async def url_handler(message: types.Message):
    if re.match(r'https?://(?:www\.)?(?:youtube\.com/.*[=/]|youtu\.be/)([\w-]+)', message.text):
        await message.answer("Ожидайте...")
        await download_youtube(url=message.text, message=message)
    elif re.match(r'https?://(?:www\.)?tiktok\.com/.*', message.text):
        await message.answer("В нынешнее время поддержка тик-тока не реализована.")
        # await download_tiktok(url=message.text, message=message)
    elif re.match(r'https?://open\.spotify\.com/track/([\w-]+)', message.text):
        await message.answer("Ожидайте...")
        await download_spotify(url=message.text, message=message)
    elif re.match(r'https?://soundcloud\.com/([\w-]+)/([\w-]+)', message.text):
        await message.answer("Ожидайте...")
        await download_soundcloud(url=message.text, message=message)
    else:
        await message.answer("Пожалуйста отправте ссылку на TikTok, YouTube, YouTube Shorts, Spotify или SoundCloud для дальнейшего скачивания")
