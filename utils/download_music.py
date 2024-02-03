import os
import requests
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
        'writethumbnail': True,  
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  
    }

    try:
        with youtube_dl.YoutubeDL(options) as ydl:
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

async def download_spotify(url, output_path="downloads", message=None):
    result = spotify.track(url)
    performers = ", ".join([artist['name'] for artist in result['artists']])
    music = result['name']

    videosSearch = VideosSearch(f'{performers} - {music}', limit=1)
    videoresult = videosSearch.result()["result"][0]["link"]

    filename = f'{output_path}/{performers}_{music}.mp3'
    thumbnail_filename = f'{output_path}/{performers}_{music}'
    
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'writethumbnail': True,  
        'outtmpl': filename,
    }

    try:
        with youtube_dl.YoutubeDL(options) as ydl:
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