import os
import youtube_dl
from aiogram import types
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from youtubesearchpython import VideosSearch

client_id = "022c2e6340fe4ce99354bbd0a3299955" 
secret = "ed1528ec956f4ef488f22b0d6236db7d"    

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)

async def download_soundcloud(url, output_path="downloads", message=None):
    # Используйте более простое имя файла без специальных символов
    filename = f'{output_path}/soundcloud_track.mp3'
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': filename,
    }

    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])

        if os.path.exists(filename) and message:
            await message.answer_audio(audio=types.InputFile(filename))
            os.remove(filename)
    except Exception as e:
        print(f"Error: {e}")

async def download_spotify(url, output_path="downloads", message=None):
    result = spotify.track(url)
    performers = ", ".join([artist['name'] for artist in result['artists']])
    music = result['name']

    videosSearch = VideosSearch(f'{performers} - {music}', limit=1)
    videoresult = videosSearch.result()["result"][0]["link"]

    filename = f'{output_path}/spotify_track.mp3'
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': filename,
    }

    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([videoresult])

        if os.path.exists(filename) and message:
            await message.answer_audio(audio=types.InputFile(filename))
            os.remove(filename)
    except Exception as e:
        print(f"Error: {e}")
