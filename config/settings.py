# Файл с настройками бота
import configparser

config = configparser.ConfigParser()

config.read('config\settings.ini')


LOG_DIR = config.get('Loging', 'LOG_DIR')
LOG_MAX_SIZE = config.getint('Loging', 'LOG_MAX_SIZE') * 1024 * 1024
LOG_BACKUP_COUNT = int(config.getint('Loging', 'LOG_BACKUP_COUNT'))
SEND_INTERVAL_MIN = config.getint('Advertising', 'SEND_INTERVAL_MIN') * 60 
USE_AD = config.getboolean('Advertising', 'USE_AD')