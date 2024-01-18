# Файл с секретными данными (токены, ключи и т.д.)
import configparser

config = configparser.ConfigParser()

config.read('config\secrets.ini')


BOT_TOKEN = config.get('Bot', 'BOT_TOKEN')
ADMIN_ID = config.get('Admin', 'ADMIN_ID')

spotify_client_id = config.get('Spotify', 'client_id')
spotify_secret = config.get('Spotify', 'secret')

X_RapidAPI_Host = config.get('TikTokApi', 'X-RapidAPI-Host')
X_RapidAPI_Key = config.get('TikTokApi', 'X-RapidAPI-Key')