import logging
import yt_dlp
import os
import re
from aiogram import types
import requests

async def download_tiktok(url, output_path="downloads", message=None):
    url = requests.get(url)
    match = re.search(r'/video/(\d+)', url.url)
    if match:
        video_id = match.group(1)

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
        try:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'video')
            filename = ydl.prepare_filename(info_dict)

            ydl.download([url])

            if os.path.exists(filename) and message:
                new_filename = f"{output_path}/{title}.mp4"
                os.rename(filename, new_filename)
                await message.answer_video(caption=title, video=types.InputFile(new_filename))
                os.remove(new_filename)
        except Exception as e:
            # Log the exception to the logger
            logging.error(f"Error downloading YouTube video: {str(e)}")