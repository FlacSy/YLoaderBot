import yt_dlp
import os
import re
from aiogram import types
import requests

async def get_tiktok_video_id(url):
    match = re.search(r'/video/(\d+)', url)
    if match:
        return match.group(1)

async def download_tiktok(url, output_path="downloads", message=None):
    response = requests.get(url)
    video_id = await get_tiktok_video_id(response.url)
    response = requests.get(f'https://tikcdn.io/ssstik/{video_id}')
    filename = f"{output_path}/{video_id}.mp4"
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
            
        if os.path.exists(filename) and message:
            await message.answer_video(video=types.InputFile(filename))
            os.remove(filename)

async def download_youtube(url, output_path="downloads", message=None):
    options = {
        'format': 'bestvideo[filesize<50M]+bestaudio/best[filesize<50M]',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', 'video')
        filename = ydl.prepare_filename(info_dict)

        ydl.download([url])

        # Check if the file exists before sending
        if os.path.exists(filename) and message:
            await message.answer_video(caption=title, video=types.InputFile(filename))
            os.remove(filename)