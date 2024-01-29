import os
import youtube_dl
from aiogram import types
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from config.secrets import spotify_client_id, spotify_secret 

auth_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)

async def download_soundcloud(url, output_path="downloads", message=None):
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'video')
            filename = ydl.prepare_filename(info_dict)

        if os.path.exists(filename) and message:
            await message.answer_audio(caption=title, audio=types.InputFile(filename))
            os.remove(filename)
    except Exception as e:
        print(f"Error: {e}")

async def download_spotify(url, output_path="downloads", message=None):
    result = spotify.track(url)
    performers = ", ".join([artist['name'] for artist in result['artists']])
    music = result['name']

    videosSearch = VideosSearch(f'{performers} - {music}', limit=1)
    videoresult = videosSearch.result()["result"][0]["link"]

    filename = f'{output_path}/{performers}_{music}.mp3'
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
