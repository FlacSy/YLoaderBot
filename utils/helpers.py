# Вспомогательные функции
import os
import logging
from aiogram import types
from aiogram.utils import executor
from config.secrets import ADMIN_ID
import datetime

async def on_startup(dp):
    # Уведомление о запуске
    logging.warning('Starting...')

# Инициализация логгера
log_file_path = os.path.join('logs', f'bot_log_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt')
logging.basicConfig(level=logging.INFO, filename=log_file_path, format='%(asctime)s - %(levelname)s - %(message)s')

async def on_shutdown(dp):
    # Уведомление о завершении работы
    logging.warning('Shutting down...')

    # Закрытие соединений (если они есть)
    await dp.storage.close()
    await dp.storage.wait_closed()
