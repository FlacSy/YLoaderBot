import configparser
from typing import Optional

config = configparser.ConfigParser()

config.read('config\secrets.ini')

BOT_TOKEN: Optional[str] = config.get('Bot', 'BOT_TOKEN', fallback=None)


SPOTIFY_CLIENT_ID: Optional[str] = config.get('Spotify', 'client_id', fallback=None)
SPOTIFY_SECRET: Optional[str] = config.get('Spotify', 'secret', fallback=None)