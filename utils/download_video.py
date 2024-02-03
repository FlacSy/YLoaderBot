import logging
import yt_dlp
import os
import re
from aiogram import types
import requests
from moviepy.editor import VideoFileClip

async def download_tiktok(url, output_path="downloads", message=None, format="mp4"):
    url = requests.get(url)
    match = re.search(r'/video/(\d+)', url.url)
    if match:
        video_id = match.group(1)
    try:
        response = requests.get(f'https://tikcdn.io/ssstik/{video_id}')
        filename = f"{output_path}/{video_id}.{format}"
        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)

            if os.path.exists(filename) and message:

                if format == "mp3":
                    mp3_filename = f"{output_path}/{video_id}.mp3"
                    await convert_video_to_mp3(filename, mp3_filename)
                    await message.answer_voice(voice=types.InputFile(mp3_filename))
                    os.remove(mp3_filename)

                elif format == "mp4":
                    await message.answer_video(video=types.InputFile(filename))  
                    os.remove(filename)
                    
        else:
            logging.error(f"Error downloading TikTok video. HTTP status code: {response.status_code}")
    except FileNotFoundError:
        logging.error(f"FileNotFoundError: The file {filename} was not found.")
    except Exception as e:
        logging.error(f"Error downloading TikTok video: {str(e)}")

async def convert_video_to_mp3(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path, codec='mp3')
    audio_clip.close()
    video_clip.close()

async def download_youtube(url, output_path="downloads", message=None, format="mp4"):
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

                if format == "mp3":
                    mp3_filename = f"{output_path}/{title}.mp3"
                    await convert_video_to_mp3(filename, mp3_filename)
                    await message.answer_voice(voice=types.InputFile(mp3_filename), caption=title)
                    os.remove(mp3_filename)

                elif format == "mp4":
                    await message.answer_video(caption=title, video=types.InputFile(filename))
                    os.remove(filename)

        except Exception as e:
            logging.error(f"Error downloading YouTube video: {str(e)}")
            logging.error(f"HTTP response: {e.response.text if e.response else 'No response'}")