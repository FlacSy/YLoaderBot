import yt_dlp
import os
from aiogram import types
import requests
from config.secrets import X_RapidAPI_Key, X_RapidAPI_Host
from aiogram.types import URLInputFile

async def download_tiktok(url, output_path="downloads", message=None):
    url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

    querystring = {"url": url}

    headers = {
        "X-RapidAPI-Key": X_RapidAPI_Key,
        "X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.get(url, headers=headers, params=querystring)

    video_link = response.json()['data']['play']

    await message.answer_video(URLInputFile(video_link))


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