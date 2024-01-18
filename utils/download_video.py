import yt_dlp
import os
from aiogram import types

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
        filename = ydl.prepare_filename(info_dict)

        ydl.download([url])

        # Check if the file exists before sending
        if os.path.exists(filename) and message:
            await message.answer_video(caption=title, video=types.InputFile(filename))
            os.remove(filename)