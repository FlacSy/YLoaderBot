# Вспомогательные функции
import os
import logging
import datetime
from logging.handlers import RotatingFileHandler
from config.settings import LOG_DIR, LOG_MAX_SIZE, LOG_BACKUP_COUNT

# Создание директории для логов, если она не существует
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Инициализация логгера с использованием RotatingFileHandler
log_file_path = os.path.join(LOG_DIR, f'bot_log_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt')
handler = RotatingFileHandler(log_file_path, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUP_COUNT, encoding='utf-8')
handler.setLevel(logging.INFO)

# Форматирование сообщений
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logging.getLogger().addHandler(handler)


async def on_shutdown(dp):
    # Уведомление о завершении работы
    logging.warning('Shutting down...')

    # Закрытие соединений (если они есть)
    await dp.storage.close()

async def on_startup(dp):
    # Уведомление о запуске
    logging.warning('Starting...')