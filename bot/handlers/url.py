import logging
import re
import os
from aiogram import types
import yt_dlp
import subprocess

async def url_handler(message: types.Message):
    if re.match(r'https?://(?:www\.)?(?:youtube\.com/.*[=/]|youtu\.be/)([\w-]+)', message.text):
        await download_youtube(url=message.text, message=message)
    elif re.match(r'https?://(?:www\.)?tiktok\.com/.*', message.text):
        await download_tiktok(url=message.text, message=message)
    else:
        await message.answer("Пожалуйста отправте ссылку на TikTik или YouTube")

async def download_tiktok(url, output_path="downloads", message=None):
    pass


async def download_youtube(url, output_path="downloads", message=None):
    options = {
        'format': 'bestvideo[filesize<50M]+bestaudio/best[filesize<50M]',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', 'video')
        filename = f'{output_path}/{title}.webm'

        ydl.download([url])

        # Check if the file exists before sending
        if os.path.exists(filename) and message:
            await message.answer_video(caption=title, video=types.InputFile(filename))
            os.remove(filename)
