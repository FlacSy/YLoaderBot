# Файл с настройками бота
import configparser

config = configparser.ConfigParser()

config.read('config\settings.ini')


LOG_DIR = config.get('Loging', 'LOG_DIR')
LOG_MAX_SIZE = config.get('Loging', 'LOG_MAX_SIZE') * 1024 * 1024
LOG_BACKUP_COUNT = config.get('Loging', 'LOG_BACKUP_COUNT')