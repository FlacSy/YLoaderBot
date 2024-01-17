# Файл с секретными данными (токены, ключи и т.д.)
import configparser

config = configparser.ConfigParser()

config.read('config\secrets.ini')


BOT_TOKEN = config.get('Bot', 'BOT_TOKEN')
ADMIN_ID = config.get('Admin', 'ADMIN_ID')

