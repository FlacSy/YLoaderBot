import os
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler
from config.settings import LOG_DIR
from typing import Any

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file_path: str = os.path.join(LOG_DIR, 'bot_log.log')
handler_file: TimedRotatingFileHandler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=2, backupCount=5, encoding='utf-8')
handler_file.setLevel(logging.INFO)

# Форматирование сообщений для файла
formatter_file: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler_file.setFormatter(formatter_file)

# Добавление обработчика к логгеру
logging.getLogger().addHandler(handler_file)

# Создание обработчика для вывода логов на консоль
handler_console = logging.StreamHandler()
handler_console.setLevel(logging.INFO)

# Форматирование сообщений для консоли
formatter_console = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler_console.setFormatter(formatter_console)

# Добавление обработчика для вывода на консоль
logging.getLogger().addHandler(handler_console)

async def on_shutdown(dp: Any) -> None:
    # Уведомление о завершении работы
    logging.warning('Shutting down...')

    # Закрытие соединений (если они есть)
    await dp.storage.close()

async def on_startup(dp: Any) -> None:
    # Уведомление о запуске
    logging.warning('Starting...')
