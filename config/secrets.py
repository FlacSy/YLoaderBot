# Файл с секретными данными (токены, ключи и т.д.)
import configparser

config = configparser.ConfigParser()

config.read('config\secrets.ini')

BOT_TOKEN = config.get('Bot', 'BOT_TOKEN')

spotify_client_id = config.get('Spotify', 'client_id')
spotify_secret = config.get('Spotify', 'secret')
