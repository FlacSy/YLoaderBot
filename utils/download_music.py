import os
import requests
import yt_dlp
from aiogram import types
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from config.secrets import SPOTIFY_CLIENT_ID, SPOTIFY_SECRET
from typing import Optional

auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_SECRET)
spotify = spotipy.Spotify(auth_manager=auth_manager)

async def download_soundcloud(url: str, output_path: str = "downloads", message: Optional[types.Message] = None) -> None:
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'writethumbnail': True,
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            ydl.download([url])

        filename = os.path.join(output_path, f"{info_dict['title']}.mp3")
        thumbnail_filename = os.path.join(output_path, f"{info_dict['title']}")

        if os.path.exists(filename) and message:
            thumbnail_path = info_dict.get('thumbnails')[-1]['url'] if 'thumbnails' in info_dict else None

            # Сохраняем обложку
            if thumbnail_path:
                thumbnail_response = requests.get(thumbnail_path)
                with open(thumbnail_filename, 'wb') as thumbnail_file:
                    thumbnail_file.write(thumbnail_response.content)

            await message.answer_audio(audio=types.InputFile(filename), thumb=types.InputFile(thumbnail_filename))

            os.remove(filename)
            os.remove(thumbnail_filename)
            os.remove(f"{thumbnail_filename}.jpg")
    except Exception as e:
        print(f"Error: {e}")

async def download_spotify(url: str, output_path: str = "downloads", message: Optional[types.Message] = None) -> None:
    result = spotify.track(url)
    performers = ", ".join([artist['name'] for artist in result['artists']])
    music = result['name']

    videosSearch = VideosSearch(f'{performers} - {music}', limit=1)
    videoresult = videosSearch.result()["result"][0]["link"]

    filename = f'{output_path}/{performers}_{music}.mp3'
    thumbnail_filename = f'{output_path}/{performers}_{music}'
    options = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(videoresult, download=False)
            ydl.download([videoresult])

        if os.path.exists(filename) and message:
            thumbnail_path = info_dict.get('thumbnails')[-1]['url'] if 'thumbnails' in info_dict else None

            if thumbnail_path:
                thumbnail_response = requests.get(thumbnail_path)
                with open(thumbnail_filename, 'wb') as thumbnail_file:
                    thumbnail_file.write(thumbnail_response.content)

            await message.answer_audio(audio=types.InputFile(filename), thumb=types.InputFile(thumbnail_filename))

        os.remove(filename)
        os.remove(thumbnail_filename)
        os.remove(f"{thumbnail_filename}.mp3.webp")
    except Exception as e:
        print(f"Error: {e}")

async def download_apple_music(url: str, output_path: str = "downloads", message: Optional[types.Message] = None) -> None:
    song_id = url.split('i=')[-1]
    api_url = f'https://itunes.apple.com/lookup?id={song_id}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        track_info = data.get('results', [])[0]

        if track_info:
            music = track_info.get('trackName')
            performers = track_info.get('artistName')

            videos_search = VideosSearch(f'{performers} - {music}', limit=1)
            video_result = videos_search.result()["result"][0]["link"]

            filename = f'{output_path}/{performers}-{music}.mp3'
            thumbnail_filename = f'{output_path}/{performers}_{music}'

            options = {
                'format': 'bestaudio/best',
                'outtmpl': filename,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                info_dict = ydl.extract_info(video_result, download=False)
                ydl.download([video_result])

            if os.path.exists(filename) and message:
                thumbnail_path = info_dict.get('thumbnails')[-1]['url'] if 'thumbnails' in info_dict else None

                if thumbnail_path:
                    thumbnail_response = requests.get(thumbnail_path)
                    with open(thumbnail_filename, 'wb') as thumbnail_file:
                        thumbnail_file.write(thumbnail_response.content)

                await message.answer_audio(audio=types.InputFile(filename), thumb=types.InputFile(thumbnail_filename))

                os.remove(filename)
                os.remove(thumbnail_filename)

        else:
            print("Информация о треке не найдена.")

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
