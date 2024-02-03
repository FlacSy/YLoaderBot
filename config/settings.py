# Файл с настройками бота
import configparser

config = configparser.ConfigParser()

config.read('config\settings.ini')


LOG_DIR = config.get('Loging', 'LOG_DIR')
SEND_INTERVAL_MIN = config.getint('Advertising', 'SEND_INTERVAL_MIN') * 60 
USE_AD = config.getboolean('Advertising', 'USE_AD')