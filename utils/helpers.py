import os
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler
from config.settings import LOG_DIR
from typing import Any

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file_path: str = os.path.join(LOG_DIR, 'bot_log.log')
handler: TimedRotatingFileHandler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=2, backupCount=5, encoding='utf-8')
handler.setLevel(logging.INFO)

# Форматирование сообщений
formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logging.getLogger().addHandler(handler)

async def on_shutdown(dp: Any) -> None:
    # Уведомление о завершении работы
    logging.warning('Shutting down...')

    # Закрытие соединений (если они есть)
    await dp.storage.close()

async def on_startup(dp: Any) -> None:
    # Уведомление о запуске
    logging.warning('Starting...')
